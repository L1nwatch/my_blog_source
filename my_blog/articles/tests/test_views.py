#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""

2016.10.03 测试视图函数是否正常
"""
import os
import unittest

from articles.forms import ArticleForm
from articles.models import Article
from articles.views import get_right_content_from_file
from my_constant import const
from django.conf import settings
from django.test import TestCase, override_settings

__author__ = '__L1n__w@tch'


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
        error_message = "显示了超过 {} 篇文章在首页了".format(const.HOME_PAGE_ARTICLES_NUMBERS)
        for i in range(const.HOME_PAGE_ARTICLES_NUMBERS + 10):
            Article.objects.create(title="test_article_{}".format(i + 1))

        response = self.client.get("/")
        counts = 0
        for article in Article.objects.all():
            article_url = "/articles/{}/".format(article.id)
            if article_url.encode("utf8") in response.content:
                counts += 1
            self.assertFalse(counts > const.HOME_PAGE_ARTICLES_NUMBERS, error_message)

    def test_home_page_uses_article_form(self):
        response = self.client.get("/")
        # 使用 assertIsInstance 确认视图使用的是正确的表单类
        self.assertIsInstance(response.context["form"], ArticleForm)
        self.assertContains(response, 'name="title"')


class DetailViewTest(TestCase):
    unique_url = "/articles/{}/"

    def test_use_article_template(self):
        Article.objects.create(title="test_article_1")
        response = self.client.get(self.unique_url.format(1))
        self.assertTemplateUsed(response, "article.html")

        # 测试是否有将 form 传递给模板
        self.assertIsInstance(response.context["form"], ArticleForm)


class AboutMeViewTest(TestCase):
    unique_url = "/articles/about_me/"

    def test_use_about_me_template(self):
        response = self.client.get(self.unique_url)
        self.assertTemplateUsed(response, "about_me.html")

    def test_view_passes_form_to_template(self):
        """
        测试是否有将 form 传递给模板
        :return:
        """
        response = self.client.get(self.unique_url)
        self.assertIsInstance(response.context["form"], ArticleForm)


class ArchivesViewTest(TestCase):
    unique_url = "/articles/archives/"

    def test_use_archives_template(self):
        response = self.client.get(self.unique_url)
        self.assertTemplateUsed(response, "archives.html")

    def test_view_passes_form_to_template(self):
        """
        测试是否有将 form 传递给模板
        :return:
        """
        response = self.client.get(self.unique_url)
        self.assertIsInstance(response.context["form"], ArticleForm)


class SearchTagViewTest(TestCase):
    unique_url = "/articles/tag{}/"

    def test_can_get_same_category(self):
        test_category_name = "test_category"
        article_1 = Article.objects.create(title="article_1", category=test_category_name)
        article_2 = Article.objects.create(title="article_2", category=test_category_name)
        article_3 = Article.objects.create(title="article_3")

        # 查找同一分类下的所有文章
        response = self.client.get(self.unique_url.format(test_category_name))
        self.assertTemplateUsed(response, "tag.html")

        # 不属于这个分类的都不会找到
        self.assertContains(response, article_1.title)
        self.assertContains(response, article_2.title)
        self.assertNotContains(response, article_3.title)

    def test_view_passes_form_to_template(self):
        """
        测试是否有将 form 传递给模板
        :return:
        """
        response = self.client.get(self.unique_url.format("just_a_test"))
        self.assertIsInstance(response.context["form"], ArticleForm)


@override_settings(UPDATE_TIME_LIMIT=0.1)
@unittest.skipUnless(const.SLOW_CONNECT_DEBUG, "值为 True 表示要进行 git 测试")
class UpdateNotesViewTest(TestCase):
    unique_url = "/articles/update_notes/"
    test_md_file_name = "测试笔记-测试用的笔记.md"

    notes_path_parent_dir = os.path.dirname(settings.BASE_DIR)
    notes_git_path = os.path.join(notes_path_parent_dir, const.NOTES_PATH_NAME)
    test_md_file_path = os.path.join(notes_git_path, test_md_file_name)

    def __update_test_md_file_and_git_push(self, test_content):
        """
        更新测试文件并将内容上传到仓库中
        :return:
        """
        with open(self.test_md_file_path, "w") as f:
            f.write(test_content)
        command = "cd {} && git add -A && git commit -m '测试开始' && git push".format(self.notes_git_path)
        os.system(command)

    def setUp(self):
        """
        主要是在测试之前备份笔记文件
        :return:
        """
        # 确保已经进行过 git 操作
        if not os.path.exists(os.path.join(self.notes_git_path, ".git")):
            self.client.get(self.unique_url)

        # 创建测试文件并上传到 git 仓库中
        self.old_file_content = "# 测试1234"
        self.__update_test_md_file_and_git_push(self.old_file_content)

    def tearDown(self):
        """
        主要是在测试结束之后恢复笔记文件
        :return:
        """
        # 删除测试文件
        command = "cd {}" \
                  " && rm {}" \
                  " && git add -A" \
                  " && git commit -m '测试完毕'" \
                  " && git push".format(self.notes_git_path, self.test_md_file_name)
        os.system(command)

    def test_can_get_md_from_git(self):
        self.client.get(self.unique_url)

        if not os.path.exists(self.test_md_file_path):
            self.fail("从 git 上获取文件失败了")

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
        self.client.get(self.unique_url)
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
        self.client.get(self.unique_url)
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
        self.client.get(self.unique_url)
        latest_article = Article.objects.get(title=test_article_title)
        self.assertEqual(latest_article.content, test_content, "数据库中依然是老文章的内容")
        self.assertEqual(latest_article.category, test_article_category, "数据库中依然是老文章的分类")

    def test_update_time_when_update_notes(self):
        # 旧的一份笔记
        test_article = self.test_md_file_name.rstrip(".md")  # 去掉 .md
        test_article_category, test_article_title = test_article.split("-")  # 去掉 "测试笔记-"
        old_article = Article.objects.create(title=test_article_title, category="old_category", content="old content")

        # 文章进行了跟新
        test_content = "# test_hello"
        self.__update_test_md_file_and_git_push(test_content)

        # 再次执行该视图函数, 发现数据库也跟着更新了, 尤其是更新时间刷新了
        self.client.get(self.unique_url)
        latest_article = Article.objects.get(title=test_article_title)
        self.assertNotEqual(old_article.update_time, latest_article.update_time)

    def test_view_passes_form_to_template(self):
        """
        测试是否有将 form 传递给模板
        :return:
        """
        response = self.client.get(self.unique_url)
        self.assertIsInstance(response.context["form"], ArticleForm)

    def test_delete_notes_from_md(self):
        """
        原先在数据库中已经存在某个笔记, 但是最新版本的 git 仓库中并没有这个笔记, 那么从数据库中删除掉
        :return:
        """
        should_not_exist_note = Article.objects.create(title="不应该存在的笔记", category="测试笔记")

        # 确认仓库中没有这个笔记
        not_exist_note_full_name = "{}-{}.md".format(should_not_exist_note.category, should_not_exist_note.title)
        self.assertNotIn(not_exist_note_full_name, os.listdir(self.notes_git_path))

        # 执行视图函数
        self.client.get(self.unique_url)

        # 发现数据库中已经不存在该笔记了
        with self.assertRaises(Article.DoesNotExist):
            Article.objects.get(title=should_not_exist_note.title)


class BlogSearchViewTest(TestCase):
    unique_url = "/articles/search/"

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post(self.unique_url, data={"title": ""})
        self.assertIsInstance(response.context["form"], ArticleForm)

    def test_for_valid_input_passes_form_to_template(self):
        response = self.client.post(self.unique_url, data={"title": "不应该有这篇文章的"})
        self.assertIsInstance(response.context["form"], ArticleForm)

    def test_form_input_not_exist_title(self):
        form = ArticleForm(data={"title": ""})
        self.assertEqual(form.errors["title"], [const.EMPTY_ARTICLE_ERROR])

    def test_view_passes_form_to_template(self):
        """
        测试是否有将 form 传递给模板
        :return:
        """
        response = self.client.get(self.unique_url)
        self.assertIsInstance(response.context["form"], ArticleForm)

    def test_valid_input_will_get_response_using_right_template(self):
        test_article = Article.objects.create(title="test_article")
        response = self.client.post(self.unique_url, data={"title": test_article.title})
        self.assertTemplateUsed(response, "search_content.html")

    def test_id_article_exist(self):
        """
        搜索存在的文章, 显示出来的界面中每篇文章应该有 id_article_title 这个属性
        :return:
        """
        test_article_title = "test_for_search_button"
        Article.objects.create(title=test_article_title)

        response = self.client.post(self.unique_url, data={"title": test_article_title})
        self.assertContains(response, 'id="id_article_title"')

    def test_can_search_content(self):
        """
        测试搜索文章的时候会去搜索文章内容
        :return:
        """
        test_article = Article.objects.create(title="test_title_文章", content="test_content")
        response = self.client.post(self.unique_url, data={"title": test_article.content})
        self.assertContains(response, test_article.title)

    def test_search_content_without_case(self):
        """
        测试搜索文章内容的时候会忽略大小写
        :return:
        """
        test_article = Article.objects.create(title="test_title_文章", content="test_content")
        response = self.client.post(self.unique_url, data={"title": "TeSt_ConTeNt"})
        self.assertContains(response, test_article.title)

    def test_can_search_content_and_title(self):
        """
        测试搜索出来的内容会从文章以及标题去查找
        :return:
        """
        test_article = Article.objects.create(title="test_title_文章", content="test_content")
        # 从标题中查找
        response = self.client.post(self.unique_url, data={"title": "title"})
        self.assertContains(response, test_article.title)

        # 从内容中查找
        response = self.client.post(self.unique_url, data={"title": "content"})
        self.assertContains(response, test_article.title)

    def test_search_multiple_words(self):
        """
        测试能够同时搜索多个关键词
        :return:
        """
        test_article = Article.objects.create(title="test_title_文章", content="test content content2")
        # 仅存在其中一个关键词
        response = self.client.post(self.unique_url, data={"title": "content3 test"})
        self.assertNotContains(response, test_article.title)

        # 两个关键词都存在
        response = self.client.post(self.unique_url, data={"title": "content2 test"})
        self.assertContains(response, test_article.title)


if __name__ == "__main__":
    pass
