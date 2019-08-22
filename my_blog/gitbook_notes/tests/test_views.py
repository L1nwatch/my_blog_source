#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 测试 gitbook_notes 这个 app 下的视图函数

2019.08.22 gitbook 链接更新了，这边也得兼容一下
2017.06.16 新增有关 GitBook 更新时会更新 Tag 的测试
2017.06.04 重构基类测试, 修改对应代码
2017.05.21 修改 common_module 路径
2017.04.30 修正大小写导致判定失误的问题, 补充完善有关 GitBook 书名的测试代码
2017.04.04 重构有关创建测试数据的代码
2017.03.23 重构了部分搜索实现, 删除了通过 URL 来区分搜索类型的相关代码
2017.03.10 发现 href 字段的 BUG, 再次补充相关测试代码
2017.03.10 发现 title 字段的 BUG, 补充相关测试代码
2017.03.05 发现依旧需要写显示页面的代码, 不过是跳转到 GitBook 罢了
2017.03.05 开始编写搜索测试代码
2017.01.28 增加了测试完毕之后删除测试文件夹的代码
2016.10.30 对更新笔记的视图函数进行测试
"""
# 标准库
import os
import random
import shutil
import unittest

from django.db import transaction
from django.test import override_settings

# 自己的模块
from articles.models import Tag
from common_module.tests.basic_test import BasicTest
from functional_tests.base import FunctionalTest
from gitbook_notes.models import GitBook
from gitbook_notes.views import (get_title_list_from_summary, get_title_and_md_file_name,
                                 get_right_href, format_title)
import my_constant as const

__author__ = '__L1n__w@tch'


class BaseCommonTest(BasicTest):
    @staticmethod
    def create_gitbooks_test_db():
        ft = FunctionalTest()
        return ft.create_gitbook_test_db_data()


@override_settings(UPDATE_TIME_LIMIT=0.1)
@unittest.skipUnless(const.SLOW_CONNECT_DEBUG, "[*] 用户选择忽略部分测试")
class UpdateGitBookCodesViewTest(BaseCommonTest):
    unique_url = const.GITBOOK_UPDATE_URL

    def setUp(self):
        """
        确保至少进行一次更新操作, 同时验证是否更新成功
        :return:
        """
        super().setUp()

        # 点击更新按钮
        self.client.get(self.unique_url)

        # 检查是否更新成功, 更新成功的标志: 每个文件夹都存在, 而且其文件夹下还有 .git
        for each_gitbook_name in self.gitbook_category_dict:
            self.assertTrue(
                os.path.exists(
                    os.path.join(self.gitbook_notes_git_path, each_gitbook_name, ".git")
                ), "找不到 .git")

    @classmethod
    def tearDownClass(cls):
        # 清除 git clone 到的文件
        if os.path.exists(cls.gitbook_notes_git_path):
            shutil.rmtree(cls.gitbook_notes_git_path)

    def test_can_save_right_book_name(self):
        """
        测试 book_name 字段的正确性
        """
        self.assertTrue(len(GitBook.objects.filter(book_name="PythonWeb".lower())) > 0)

    def test_can_save_right_href(self):
        """
        测试 href 字段的正确性
        """
        # 测试 href1
        gitbook = GitBook.objects.get(title="《PythonWeb 开发: 测试驱动方法》-准备工作和应具备的知识")
        right_href = ("https://l1nwatch.gitbook.io/pythonweb/pythonweb-kai-fa-ce-shi-qu-dong-fang-fa/"
                      "zhun-bei-gong-zuo-he-ying-ju-bei-de-zhi-shi/")
        self.assertEqual(gitbook.href, right_href)

        # 测试 href2
        gitbook = GitBook.objects.get(title="《PythonWeb 开发: 测试驱动方法》-第一部分 tdd 和 django 基础/第 1 章 使用功能测试协助安装 django")
        right_href = ("https://l1nwatch.gitbook.io/pythonweb/pythonweb-kai-fa-ce-shi-qu-dong-fang-fa/"
                      "di-yi-bu-fen-tdd-he-django-ji-chu/di-1-zhang-shi-yong-gong-neng-ce-shi-xie-zhu-an-zhuang-django/")
        self.assertEqual(gitbook.href, right_href)

        # 测试 href3
        gitbook = GitBook.objects.get(title="《PythonWeb 开发: 测试驱动方法》-第二部分 web 开发要素/第 14 章 部署新代码")
        right_href = ("https://l1nwatch.gitbook.io/pythonweb/pythonweb-kai-fa-ce-shi-qu-dong-fang-fa/"
                      "di-er-bu-fen-web-kai-fa-yao-su/di-14-zhang-bu-shu-xin-dai-ma/")
        self.assertEqual(gitbook.href, right_href)

    def test_can_save_right_title(self):
        """
        测试 title 字段的正确性
        """
        os.path.exists(os.path.join(self.gitbook_notes_git_path, "PythonWeb开发: 测试驱动方法", "准备工作和应具备的知识", "readme.md"))

        self.assertIsNotNone(GitBook.objects.get(title="《PythonWeb 开发: 测试驱动方法》-准备工作和应具备的知识"))

    def test_can_save_right_content(self):
        """
        测试 content 字段的正确性
        """
        test_file_path = os.path.join(self.gitbook_notes_git_path, "PythonWeb", "PythonWeb开发: 测试驱动方法",
                                      "准备工作和应具备的知识", "readme.md")
        with open(test_file_path, "r") as f:
            data = f.read()

        content_in_db = GitBook.objects.get(title="《PythonWeb 开发: 测试驱动方法》-准备工作和应具备的知识")
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

    def test_get_title_list_from_summary(self):
        """
        测试函数是否获取 summary.md 信息正确
        """
        summary_path = os.path.join(self.gitbook_notes_git_path, "PythonWeb", "SUMMARY.md")
        title_list = get_title_list_from_summary(summary_path)

        self.assertIn("PythonWeb开发: 测试驱动方法/准备工作和应具备的知识/readme.md", title_list)
        self.assertIn("PythonWeb开发: 测试驱动方法/第一部分 TDD 和 Django 基础/readme.md", title_list)
        self.assertIn("PythonWeb开发: 测试驱动方法/第一部分 TDD 和 Django 基础/第 1 章 使用功能测试协助安装 Django/readme.md", title_list)
        self.assertIn("PythonWeb开发: 测试驱动方法/附录/readme.md", title_list)
        self.assertIn("PythonWeb开发: 测试驱动方法/附录/附录 D 测试数据库迁移/readme.md", title_list)

    def test_can_save_right_tag(self):
        """
        测试更新的时候可以正确保存 tag 字段
        """
        test_tag_name = "Python"
        test_tag, created = Tag.objects.get_or_create(tag_name=test_tag_name)
        gitbooks = GitBook.objects.filter(tag=test_tag)

        # 存在至少一篇笔记
        self.assertTrue(len(gitbooks) > 0)


class GitBookSearchViewTest(BaseCommonTest):
    unique_url = const.SEARCH_URL

    def test_use_right_template_to_show_search_result(self):
        """
        日记搜索用的模板应该和 articles APP 用的一样
        """
        response = self.client.post(self.unique_url, data={"search_content": "随便输入了一些什么",
                                                           "search_choice": "gitbooks"})
        self.assertTemplateUsed(response, "search_result.html")

    def test_search_result_display(self):
        """
        测试搜索出来能够显示 GitBook 的标题和结果
        """
        gitbook, _ = self.create_gitbooks_test_db()

        response = self.client.post(self.unique_url, data={"search_content": gitbook.content,
                                                           "search_choice": "gitbooks"})
        self.assertContains(response, gitbook.title)
        self.assertContains(response, gitbook.content)

    def test_journal_href_right(self):
        """
        测试搜索出来的 GitBook 链接正确
        """
        gitbook, _ = self.create_gitbooks_test_db()

        response = self.client.post(self.unique_url, data={"search_content": gitbook.content,
                                                           "search_choice": "gitbooks"})

        self.assertContains(response, "/gitbook_notes/{}/".format(gitbook.id))

    def test_search_multiple_keywords(self):
        """
        测试同时搜索多个关键词, 且能忽略大小写, 能搜索出来结果
        """
        gitbook, _ = self.create_gitbooks_test_db()

        #  GitBook <test_book_name> 里面有一章是 <test>, 内容为 <test content>
        response = self.client.post(self.unique_url, data={"search_content": "conTent teSt",
                                                           "search_choice": "gitbooks"})

        self.assertContains(response, gitbook.title)


class GitBookPageDisplayTest(BaseCommonTest):
    unique_url = const.GITBOOK_DISPLAY_URL

    def test_display_href_redirect(self):
        """
        测试是否有跳转到 GitBook 的链接
        """
        gitbooks = self.create_gitbooks_test_db()

        gitbook = GitBook.objects.get(title=random.choice(gitbooks))

        response = self.client.get(self.unique_url.format(gitbook.id))
        self.assertEqual(response.url, gitbook.href)

    def test_get_title_and_md_file_name(self):
        """
        测试几种情况下得到的 title 字段是否正确
        """
        # 情况 1, 直接就是 md 文件名
        book_name = "《PythonWeb 开发: 测试驱动方法》"
        test_data = "第1章入门.md", book_name
        right_answer = "{}-第1章入门".format(book_name), "第1章入门.md"
        my_answer = get_title_and_md_file_name(*test_data)
        self.assertEqual(my_answer, right_answer)

        # 情况 2, 一级下的 title
        test_data = "腾讯 2017 暑期实习生编程题/腾讯 2017 暑期实习生编程题.md", book_name
        right_answer = "{}-腾讯 2017 暑期实习生编程题/腾讯 2017 暑期实习生编程题".format(book_name), "腾讯 2017 暑期实习生编程题.md"
        my_answer = get_title_and_md_file_name(*test_data)
        self.assertEqual(my_answer, right_answer)

        # 情况 3, 多级下的 readme
        test_data = "PythonWeb开发: 测试驱动方法/readme.md", book_name
        right_answer = "{}".format(book_name), "readme.md"
        my_answer = get_title_and_md_file_name(*test_data)
        self.assertEqual(my_answer, right_answer)

        # 情况 4, 多级下的 md
        test_data = "网易 2017 校招笔试编程题/二进制权重.md", book_name
        right_answer = "{}-网易 2017 校招笔试编程题/二进制权重".format(book_name), "二进制权重.md"
        my_answer = get_title_and_md_file_name(*test_data)
        self.assertEqual(my_answer, right_answer)

        # 情况 5, 书名已存在于路径之中
        test_data = "PythonWeb开发: 测试驱动方法/准备工作和应具备的知识/readme.md", book_name
        right_answer = "{}-准备工作和应具备的知识".format(book_name), "readme.md"
        my_answer = get_title_and_md_file_name(*test_data)
        self.assertEqual(my_answer, right_answer)

    def test_format_title(self):
        # 情况 1, 包含书名
        book_name = "《PythonWeb 开发: 测试驱动方法》"
        test_data = "PythonWeb开发: 测试驱动方法/准备工作和应具备的知识/readme"
        right_answer = "{}-准备工作和应具备的知识".format(book_name)
        my_answer = format_title(test_data, book_name)
        self.assertEqual(right_answer, my_answer)

        # 情况 2, 不包含书名
        test_data = "准备工作和应具备的知识/readme"
        right_answer = "{}-准备工作和应具备的知识".format(book_name)
        my_answer = format_title(test_data, book_name)
        self.assertEqual(right_answer, my_answer)

        # 情况 3, 包含书名, 且只有 readme
        test_data = "PythonWeb开发: 测试驱动方法/readme"
        right_answer = "{}".format(book_name)
        my_answer = format_title(test_data, book_name)
        self.assertEqual(right_answer, my_answer)

    def test_get_right_href(self):
        """
        测试计算 gitbook 的 href 是否正确
        """
        # 1、含有 readme 的一级
        test_data = ("interview_exercise", "README.md")
        right_href = "https://l1nwatch.gitbook.io/interview_exercise/"
        my_answer = get_right_href(*test_data)
        self.assertEqual(right_href, my_answer)

        # 2、含有 readme 的多级
        test_data = ("interview_exercise",
                     "计算机知识/readme.md")
        right_href = "https://l1nwatch.gitbook.io/interview_exercise/ji-suan-ji-zhi-shi/"
        my_answer = get_right_href(*test_data)
        self.assertEqual(right_href, my_answer)

        # 3、含有 readme 的多级 2
        test_data = ("PythonWeb",
                     "PythonWeb开发: 测试驱动方法/准备工作和应具备的知识/readme.md")
        right_href = ("https://l1nwatch.gitbook.io/pythonweb/pythonweb-kai-fa-ce-shi-qu-dong-fang-fa/"
                      "zhun-bei-gong-zuo-he-ying-ju-bei-de-zhi-shi/")
        my_answer = get_right_href(*test_data)
        self.assertEqual(right_href, my_answer)

        # 4、不含 readme 的一级
        test_data = ("interview_exercise",
                     "C_问答题汇总.md")
        right_href = "https://l1nwatch.gitbook.io/interview_exercise/c-wen-da-ti-hui-zong"
        my_answer = get_right_href(*test_data)
        self.assertEqual(right_href, my_answer)

        # 5、不含 readme 的多级
        test_data = ("interview_exercise",
                     "stackoverflow-about-Python/Python中如何在一个函数中加入多个装饰器.md")
        right_href = ("https://l1nwatch.gitbook.io/interview_exercise/stackoverflow-about-python/"
                      "python-zhong-ru-he-zai-yi-ge-han-shu-zhong-jia-ru-duo-ge-zhuang-shi-qi")
        my_answer = get_right_href(*test_data)
        self.assertEqual(right_href, my_answer)
