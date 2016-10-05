#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""

2016.10.03 测试视图函数是否正常
"""
from django.test import TestCase
from django.conf import settings

from articles.models import Article
from articles.views import HOME_PAGE_ARTICLES_NUMBERS

import os

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


class UpdateNotesViweTest(TestCase):
    test_md_file_name = "测试笔记-测试用的笔记.md"
    notes_path_name = "notes"
    notes_path_parent_dir = os.path.dirname(settings.BASE_DIR)

    notes_git_path = os.path.join(notes_path_parent_dir, notes_path_name)
    test_md_file_path = os.path.join(notes_git_path, test_md_file_name)

    def test_can_get_md_from_git(self):
        self.client.get("/articles/update_notes/")

        if not os.path.exists(self.test_md_file_path):
            self.fail("从 git 上获取文件失败了")

    def test_can_sync_md_from_git(self):
        """
        确保获取到的是 git 上的最新版本
        :return:
        """
        # 已经进行过 git 操作
        if not os.path.exists(os.path.join(self.notes_git_path, ".git")):
            self.client.get("/articles/update_notes/")

        # 保存旧的测试文件
        with open(self.test_md_file_path, "r") as f:
            old_file_content = f.read()

        # 更改文件夹中的测试文件, git 提交到仓库上
        with open(self.test_md_file_path, "w") as f:
            test_content = "# test1234"
            f.write(test_content)
        command = "cd {} && git commit && git push".format(self.notes_git_path)
        os.system(command)

        # 恢复旧的测试文件
        with open(self.test_md_file_path, "w") as f:
            f.write(old_file_content)

        # 再次执行该视图函数, 发现文件夹里的旧测试文件已经变成新的测试文件了
        self.client.get("/articles/update_notes/")
        with open(self.test_md_file_path, "r") as f:
            data = f.read()
        try:
            self.assertEqual(data, test_content, "更新测试文件失败")
        except AssertionError:
            raise AssertionError
        finally:
            print("[*] 成功执行了这一句")
            # 恢复测试文件, 提交内容
            with open(self.test_md_file_path, "w") as f:
                f.write(old_file_content)
            command = "cd {} && git commit && git push".format(self.notes_git_path)
            os.system(command)


if __name__ == "__main__":
    pass
