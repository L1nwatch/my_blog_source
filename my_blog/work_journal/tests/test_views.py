#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.02.03 开始写这个 APP, 需要新建单元测试
"""
from work_journal.forms import JournalForm
from work_journal.models import Journal
from my_constant import const
from django.test import TestCase
from django.conf import settings

import os

__author__ = '__L1n__w@tch'


class JournalHomeViewTest(TestCase):
    unique_url = "/work_journal/"

    def test_use_right_template(self):
        """
        测试使用了正确的模板文件
        """
        response = self.client.get(self.unique_url)
        self.assertTemplateUsed(response, "journal_home.html")

    def test_use_journal_form(self):
        """
        测试使用了 JournalForm 表单类
        """
        response = self.client.get(self.unique_url)
        # 使用 assertIsInstance 确认视图使用的是正确的表单类
        self.assertIsInstance(response.context["form"], JournalForm)
        self.assertContains(response, 'name="title"')

    def test_display_all_journals(self):
        """
        测试显示了所有 journal 而不只是某几篇
        """
        test_journals_number = 10

        # 测试 10 篇文章
        for i in range(test_journals_number):
            Journal.objects.create(title="test_journal_{}".format(i + 1))

        response = self.client.get(self.unique_url)
        counts = 0
        for journal in Journal.objects.all():
            journal_url = "{}{}/".format(self.unique_url, journal.id)
            if journal_url.encode("utf8") in response.content:
                counts += 1
        self.assertEqual(counts, test_journals_number)

    def test_no_display_journal_content(self):
        """
        测试日常汇总首页不显示日记的内容
        """
        journal = Journal.objects.create(title="test_journal_1", content="test_journal_content_1")
        response = self.client.get(self.unique_url)
        self.assertNotContains(response, journal.content)

    def test_title_with_href(self):
        """
        测试显示的日记, 每一篇都带有超链接, 链接到对应的日记 url
        """
        journal = Journal.objects.create(title="test_journal_1", content="test_journal_content_1")
        response = self.client.get(self.unique_url)

        # 标题存在
        self.assertContains(response, journal.title)

        # 对应的链接 url 也存在
        self.assertContains(response, "{}{}/".format(self.unique_url, journal.id))


class JournalDisplayViewTest(TestCase):
    unique_url = "/work_journal/{}/"

    def setUp(self):
        super().__init__()

        self._create_journal_test_db()

    @staticmethod
    def _create_journal_test_db():
        # 创建一篇普通的日记
        Journal.objects.create(title="test_journal_1", content="test_journal_content_1")

        # 创建一篇 Markdown 格式的日记
        with open(os.path.join(settings.BASE_DIR, "markdown_file_for_test.md"), "r") as f:
            content = f.read()

        Journal.objects.create(title="test_journal_with_markdown", content=content)

    def test_use_right_template(self):
        """
        测试使用了正确的模板文件
        """
        journal = Journal.objects.get(id=1)

        response = self.client.get(self.unique_url.format(journal.id))
        self.assertTemplateUsed(response, "journal_display.html")

    def test_display_content(self):
        """
        测试是否有把文章的内容显示出来
        """
        journal = Journal.objects.get(id=1)

        response = self.client.get(self.unique_url.format(journal.id))
        self.assertContains(response, journal.content)

    def test_markdown_display(self):
        """
        测试文章是否成功解析 markdown 了, 通过区分 # 号来判断
        """
        markdown_journal = Journal.objects.get(title="test_journal_with_markdown")

        # markdown 格式的内容存在于数据库里
        self.assertIn("## 二级标题", markdown_journal.content)

        # 但是页面上只存在解析后的内容
        response = self.client.get(self.unique_url.format(markdown_journal.id))
        self.assertContains(response, "二级标题")
        self.assertNotContains(response, "## 二级标题")


if __name__ == "__main__":
    pass
