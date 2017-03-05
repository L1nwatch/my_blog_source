#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 测试 gitbook_notes 这个 app 下的视图函数

2017.03.05 发现依旧需要写显示页面的代码, 不过是跳转到 GitBook 罢了
2017.03.05 开始编写搜索测试代码
2017.01.28 增加了测试完毕之后删除测试文件夹的代码
2016.10.30 对更新笔记的视图函数进行测试
"""
from functional_tests.base import FunctionalTest
from django.test import TestCase, override_settings
from my_constant import const
from gitbook_notes.models import GitBook
from gitbook_notes.views import get_title_list_from_summary

import os
import unittest
import shutil

__author__ = '__L1n__w@tch'


class BaseCommonTest(TestCase):
    @staticmethod
    def create_gitbooks_test_db():
        FunctionalTest.create_gitbook_test_db_data()


@override_settings(UPDATE_TIME_LIMIT=0.1)
@unittest.skipUnless(const.SLOW_CONNECT_DEBUG, "const.SLOW_CONNECT_DEBUG 值为 True 才表示要进行 git 测试")
class UpdateGitBookCodesViewTest(TestCase):
    unique_url = "/gitbook_notes/update_gitbook_codes/"
    gitbook_category_dict = const.GITBOOK_CODES_REPOSITORY
    notes_git_path = const.GITBOOK_CODES_PATH

    def setUp(self):
        """
        确保至少进行一次更新操作, 同时验证是否更新成功
        :return:
        """
        super().setUp()

        # TODO: 通过测试后删除并取消 tearDown 的注释
        self.client.get(self.unique_url)

        # 通过判断文件夹是否存在, 如果不存在则点击更新按钮
        for each_gitbook_name in self.gitbook_category_dict:
            if not os.path.exists(os.path.join(self.notes_git_path, each_gitbook_name)):
                self.client.get(self.unique_url)

        # 检查是否更新成功, 更新成功的标志: 每个文件夹都存在, 而且其文件夹下还有 .git
        for each_gitbook_name in self.gitbook_category_dict:
            self.assertTrue(
                os.path.exists(
                    os.path.join(self.notes_git_path, each_gitbook_name, ".git")
                ), "找不到 .git")

    def test_can_save_right_book_name(self):
        """
        测试 book_name 字段的正确性
        """
        self.assertTrue(len(GitBook.objects.filter(book_name="PythonWeb")) > 0)

    def test_can_save_right_href(self):
        """
        测试 href 字段的正确性
        """
        # 测试 href1
        gitbook = GitBook.objects.get(title="PythonWeb开发: 测试驱动方法/准备工作和应具备的知识")
        right_href = ("https://l1nwatch.gitbooks.io/pythonweb/content/"
                      "PythonWeb%E5%BC%80%E5%8F%91%3A%20%E6%B5%8B%E8%AF%95%E9%A9%B1%E5%8A%A8%E6%96%B9%E6%B3%95/"
                      "%E5%87%86%E5%A4%87%E5%B7%A5%E4%BD%9C%E5%92%8C%E5%BA%94%E5%85%B7%E5%A4%87%E7%9A%84%E7%9F"
                      "%A5%E8%AF%86/readme.html")
        self.assertEqual(gitbook.href, right_href)

        # 测试 href2
        gitbook = GitBook.objects.get(title="PythonWeb开发: 测试驱动方法/第一部分 TDD 和 Django 基础/第 1 章 使用功能测试协助安装 Django")
        right_href = ("https://l1nwatch.gitbooks.io/pythonweb/content/PythonWeb"
                      "%E5%BC%80%E5%8F%91%3A%20%E6%B5%8B%E8%AF%95%E9%A9%B1%E5%8A%A8%E6%96%B9%E6%B3%95/"
                      "%E7%AC%AC%E4%B8%80%E9%83%A8%E5%88%86%20TDD%20%E5%92%8C%20Django"
                      "%20%E5%9F%BA%E7%A1%80/%E7%AC%AC%201%20%E7%AB%A0%20%E4%BD%BF%E7%94%A8%E5%8A%9F%E8%83%BD%E6"
                      "%B5%8B%E8%AF%95%E5%8D%8F%E5%8A%A9%E5%AE%89%E8%A3%85%20Django/readme.html")
        self.assertEqual(gitbook.href, right_href)

        # 测试 href3
        gitbook = GitBook.objects.get(title="PythonWeb开发: 测试驱动方法/第二部分 Web 开发要素/第 14 章 部署新代码")
        right_href = ("https://l1nwatch.gitbooks.io/pythonweb/content/PythonWeb"
                      "%E5%BC%80%E5%8F%91%3A%20%E6%B5%8B%E8%AF%95%E9%A9%B1%E5%8A%A8%E6%96%B9%E6%B3%95/"
                      "%E7%AC%AC%E4%BA%8C%E9%83%A8%E5%88%86%20Web%20%E5%BC%80%E5%8F%91%E8%A6%81%E7%B4%A0/"
                      "%E7%AC%AC%2014%20%E7%AB%A0%20%E9%83%A8%E7%BD%B2%E6%96%B0%E4%BB%A3%E7%A0%81/readme.html")
        self.assertEqual(gitbook.href, right_href)

    def test_can_save_right_title(self):
        """
        测试 title 字段的正确性
        """
        os.path.exists(os.path.join(self.notes_git_path, "PythonWeb开发: 测试驱动方法", "准备工作和应具备的知识", "readme.md"))

        self.assertIsNotNone(GitBook.objects.get(title="PythonWeb开发: 测试驱动方法/准备工作和应具备的知识"))

    def test_can_save_right_content(self):
        """
        测试 content 字段的正确性
        """
        test_file_path = os.path.join(self.notes_git_path, "PythonWeb", "PythonWeb开发: 测试驱动方法",
                                      "准备工作和应具备的知识", "readme.md")
        with open(test_file_path, "r") as f:
            data = f.read()

        content_in_db = GitBook.objects.get(title="PythonWeb开发: 测试驱动方法/准备工作和应具备的知识")
        self.assertEqual(content_in_db.content, data)

    def test_can_save_right_md_file_name(self):
        """
        测试 md_file_name 字段的正确性
        """
        # 根目录下的 SUMMARY.md 应该是不会保存到数据库中的
        with self.assertRaises(GitBook.DoesNotExist):
            GitBook.objects.get(md_file_name="SUMMARY.md")

        # 根目录下的 readme.md 应该是会保存到数据库中的, 而且搜 readme.md 应该出来不止一个
        readme_md = GitBook.objects.filter(md_file_name="readme.md")
        self.assertTrue(len(readme_md) > 1)




        # @classmethod
        # def tearDownClass(cls):
        # 清除 git clone 到的文件
        # if os.path.exists(cls.notes_git_path):
        #     shutil.rmtree(cls.notes_git_path)

    def test_get_title_list_from_summary(self):
        """
        测试函数是否获取正确
        """
        summary_path = os.path.join(self.notes_git_path, "PythonWeb", "SUMMARY.md")
        title_list = get_title_list_from_summary(summary_path)

        self.assertIn("PythonWeb开发: 测试驱动方法/准备工作和应具备的知识/readme.md", title_list)
        self.assertIn("PythonWeb开发: 测试驱动方法/第一部分 TDD 和 Django 基础/readme.md", title_list)
        self.assertIn("PythonWeb开发: 测试驱动方法/第一部分 TDD 和 Django 基础/第 1 章 使用功能测试协助安装 Django/readme.md", title_list)
        self.assertIn("PythonWeb开发: 测试驱动方法/附录/readme.md", title_list)
        self.assertIn("PythonWeb开发: 测试驱动方法/附录/附录 D 测试数据库迁移/readme.md", title_list)


class GitBookSearchViewTest(BaseCommonTest):
    unique_url = "/search/search_type=gitbooks"

    def test_use_right_template_to_show_search_result(self):
        """
        日记搜索用的模板应该和 articles APP 用的一样
        """
        response = self.client.post(self.unique_url, data={"title": "随便输入了一些什么"})
        self.assertTemplateUsed(response, "search_result.html")

    def test_search_result_display(self):
        """
        测试搜索出来能够显示 GitBook 的标题和结果
        """
        self.create_gitbooks_test_db()

        gitbook = GitBook.objects.get(title="test_book_name/test")
        response = self.client.post(self.unique_url, data={"title": gitbook.content})
        self.assertContains(response, gitbook.title)
        self.assertContains(response, gitbook.content)

    def test_journal_href_right(self):
        """
        测试搜索出来的 GitBook 链接正确
        """
        self.create_gitbooks_test_db()

        gitbook = GitBook.objects.get(title="test_book_name/test")
        response = self.client.post(self.unique_url, data={"title": gitbook.content})

        self.assertContains(response, "/gitbook_notes/{}/".format(gitbook.id))

    def test_search_multiple_keywords(self):
        """
        测试同时搜索多个关键词, 且能忽略大小写, 能搜索出来结果
        """
        self.create_gitbooks_test_db()

        #  GitBook <test_book_name> 里面有一章是 <test>, 内容为 <test content>
        gitbook = GitBook.objects.get(title="test_book_name/test")
        response = self.client.post(self.unique_url, data={"title": "conTent teSt"})

        self.assertContains(response, gitbook.title)


class GitBookPageDisplayTest(BaseCommonTest):
    unique_url = "/gitbook_notes/{}/"

    def test_display_href_redirect(self):
        """
        测试是否有跳转到 GitBook 的链接
        """
        self.create_gitbooks_test_db()

        gitbook = GitBook.objects.get(title="stackoverflow-about-Python/super与init方法")

        response = self.client.get(self.unique_url.format(gitbook.id))
        self.assertEqual(response.url, gitbook.href)


if __name__ == "__main__":
    pass
