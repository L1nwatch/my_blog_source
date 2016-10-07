#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""

2016.10.03 测试视图函数是否正常
"""
from django.test import TestCase
from django.conf import settings
from articles.models import Article
from articles.views import HOME_PAGE_ARTICLES_NUMBERS, get_right_content_from_file

import os
import unittest

__author__ = '__L1n__w@tch'

TEST_GIT_REPOSITORY = settings.TEST_GIT_REPOSITORY


class HomeViewTest(TestCase):
    def test_use_home_template(self):
        """
        测试是否使用了首页的模板
        :return:
        """
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_only_display_part_articles(self):
        """
        测试是否只显示了部分的文章, 而不是显示所有文章
        :return:
        """
        error_message = "显示了超过 {} 篇文章在首页了".format(HOME_PAGE_ARTICLES_NUMBERS)
        for i in range(HOME_PAGE_ARTICLES_NUMBERS + 10):
            Article.objects.create(title="test_article_{}".format(i + 1))

        response = self.client.get("/")
        counts = 0
        for article in Article.objects.all():
            article_url = "/articles/{}/".format(article.id)
            if article_url.encode("utf8") in response.content:
                counts += 1
            self.assertFalse(counts > HOME_PAGE_ARTICLES_NUMBERS, error_message)


class DetailViewTest(TestCase):
    def test_use_article_template(self):
        Article.objects.create(title="test_article_1")
        response = self.client.get("/articles/{}/".format(1))
        self.assertTemplateUsed(response, "article.html")


class AboutMeViewTest(TestCase):
    def test_use_about_me_template(self):
        response = self.client.get("/articles/about_me/")
        self.assertTemplateUsed(response, "about_me.html")


class ArchivesViewTest(TestCase):
    def test_use_archives_template(self):
        response = self.client.get("/articles/archives/")
        self.assertTemplateUsed(response, "archives.html")


class SearchTagViewTest(TestCase):
    def test_can_get_same_category(self):
        test_category_name = "test_category"
        article_1 = Article.objects.create(title="article_1", category=test_category_name)
        article_2 = Article.objects.create(title="article_2", category=test_category_name)
        article_3 = Article.objects.create(title="article_3")

        # 查找同一分类下的所有文章
        response = self.client.get("/articles/tag{}/".format(test_category_name))
        self.assertTemplateUsed(response, "tag.html")

        # 不属于这个分类的都不会找到
        self.assertContains(response, article_1.title)
        self.assertContains(response, article_2.title)
        self.assertNotContains(response, article_3.title)


class UpdateNotesViewTest(TestCase):
    test_md_file_name = "测试笔记-测试用的笔记.md"
    notes_path_name = "notes"
    global_want_to_run_git_test = input("确定要进行 git 测试?(yes?)")

    notes_path_parent_dir = os.path.dirname(settings.BASE_DIR)
    notes_git_path = os.path.join(notes_path_parent_dir, notes_path_name)
    test_md_file_path = os.path.join(notes_git_path, test_md_file_name)

    def setUp(self):
        """
        主要是在测试之前备份笔记文件
        :return:
        """
        # 确保已经进行过 git 操作
        if not os.path.exists(os.path.join(self.notes_git_path, ".git")):
            self.client.get("/articles/update_notes/")

        # 保存旧的测试文件
        self.old_file_content = get_right_content_from_file(self.test_md_file_path)

    def tearDown(self):
        """
        主要是在测试结束之后恢复笔记文件
        :return:
        """
        # 恢复测试文件, 提交内容
        with open(self.test_md_file_path, "w") as f:
            f.write(self.old_file_content)
        command = "cd {} && git add -A && git commit -m '测试完毕' && git push".format(self.notes_git_path)
        os.system(command)

    def __update_test_md_file_and_git_push(self, test_content):
        """
        更新测试文件并将内容上传到仓库中
        :return:
        """
        with open(self.test_md_file_path, "w") as f:
            f.write(test_content)
        command = "cd {} && git add -A && git commit -m '测试开始' && git push".format(self.notes_git_path)
        os.system(command)

    @unittest.skipUnless(global_want_to_run_git_test == "yes", "决定进行 git 测试")
    def test_can_get_md_from_git(self):
        self.client.get("/articles/update_notes/")

        if not os.path.exists(self.test_md_file_path):
            self.fail("从 git 上获取文件失败了")

    @unittest.skipUnless(global_want_to_run_git_test == "yes", "决定进行 git 测试")
    def test_can_sync_md_from_git(self):
        """
        确保获取到的是 git 上的最新版本
        :return:
        """
        # 更改文件夹中的测试文件, git 提交到仓库上
        test_content = "# test1234"
        self.__update_test_md_file_and_git_push(test_content)

        # 恢复旧的测试文件
        with open(self.test_md_file_path, "w") as f:
            f.write(self.old_file_content)

        # 再次执行该视图函数, 发现文件夹里的旧测试文件已经变成新的测试文件了
        self.client.get("/articles/update_notes/")
        data = get_right_content_from_file(self.test_md_file_path)
        self.assertEqual(data, test_content, "更新测试文件失败")

    def test_create_notes_from_md(self):
        # 每个 md 笔记的文件名类似于: "测试笔记-测试用的笔记.md"
        test_article = self.test_md_file_name.rstrip(".md")  # 去掉 .md
        test_article_title = test_article.split("-")[1]  # 去掉 "测试笔记-"
        test_article_content = get_right_content_from_file(self.test_md_file_path)
        article = None

        # 一开始没有这篇文章
        with self.assertRaises(Article.DoesNotExist):
            article = Article.objects.get(title=test_article_title)
        self.assertEqual(article, None, "一开始不应该有这篇文章的")

        # 执行完该视图函数之后就有了
        self.client.get("/articles/update_notes/")
        try:
            article = Article.objects.get(title=test_article_title)
            self.assertTrue(article is not None, "没有成功更新数据库啊")
            self.assertEqual(article.content, test_article_content, "文件内容不对啊")
        except Article.DoesNotExist:
            self.fail("没有成功更新数据库啊")

    def test_update_notes_from_md(self):
        # 每个 md 笔记的文件名类似于: "测试笔记-测试用的笔记.md"
        test_article = self.test_md_file_name.rstrip(".md")  # 去掉 .md
        test_article_category, test_article_title = test_article.split("-")  # 去掉 "测试笔记-"
        Article.objects.create(title=test_article_title, category="old_category", content="old content")

        # 文章进行了更新
        test_content = "# test_hello"
        self.__update_test_md_file_and_git_push(test_content)

        # 再次执行该视图函数, 发现数据库也跟着更新了
        self.client.get("/articles/update_notes/")
        latest_article = Article.objects.get(title=test_article_title)
        self.assertEqual(latest_article.content, test_content, "数据库中依然是老文章的内容")
        self.assertEqual(latest_article.category, test_article_category, "数据库中依然是老文章的分类")

        # 文章被删除了
        # self.fail("编写单元测试中")

        # 再次执行该视图函数, 发现数据库中该文章也不见了

        pass


class BlogSearchViewTest(TestCase):
    def test_post_data_success(self):
        pass

    def test_not_post_data_will_return_to_home_page(self):
        pass

    def test_post_success_will_use_archives_template(self):
        pass


if __name__ == "__main__":
    pass
