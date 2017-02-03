#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.02.03 开始写这个 APP, 需要新建单元测试
"""
import unittest
import shutil

from work_journal.forms import JournalForm
from work_journal.models import Journal
from articles.views import get_right_content_from_file
from my_constant import const
from django.test import TestCase, override_settings
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


@override_settings(UPDATE_TIME_LIMIT=0.1)
@unittest.skipUnless(const.SLOW_CONNECT_DEBUG, "const.SLOW_CONNECT_DEBUG 值为 True 才表示要进行 git 测试")
class UpdateNotesViewTest(TestCase):
    unique_url = "/work_journal/update_journals/"
    test_md_file_name = "2017-02-03-任务情况总结测试笔记.md"  # 注意这里不能有空格, 要不然 git 命令就失败了...

    journals_git_path = os.path.join(const.NOTES_PATH_PARENT_DIR, const.JOURNALS_PATH_NAME)
    test_md_file_path = os.path.join(journals_git_path, test_md_file_name)

    def __update_test_md_file_and_git_push(self, test_content):
        """
        更新测试文件并将内容上传到仓库中
        """
        with open(self.test_md_file_path, "w") as f:
            f.write(test_content)
        command = "cd {} && git add -A && git commit -m '测试开始' && git push".format(self.journals_git_path)
        os.system(command)

    def setUp(self):
        """
        主要是在测试之前备份笔记文件
        :return:
        """
        # 确保已经进行过 git 操作
        if not os.path.exists(os.path.join(self.journals_git_path, ".git")):
            self.client.get(self.unique_url)

        # 判断是否 git 成功了
        self.assertTrue(os.path.exists(os.path.join(self.journals_git_path, ".git")), "没 git 成功啊")

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
                  " && git push".format(self.journals_git_path, self.test_md_file_name)
        os.system(command)

        # 删除整个 notes 测试文件夹
        shutil.rmtree(const.JOURNALS_GIT_PATH)

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
        # 每个 md 笔记的文件名类似于: "2017-02-03 任务情况总结.md"
        test_journal_title = self.test_md_file_name.rstrip(".md")  # 去掉 .md
        test_journal_content = get_right_content_from_file(self.test_md_file_path)
        journal = None

        # 一开始没有这篇文章
        with self.assertRaises(Journal.DoesNotExist):
            journal = Journal.objects.get(title=test_journal_title)
        self.assertEqual(journal, None, "一开始不应该有这篇文章的")

        # 执行完该视图函数之后就有了
        self.client.get(self.unique_url)
        try:
            journal = Journal.objects.get(title=test_journal_title)
            self.assertTrue(journal is not None, "没有成功更新数据库啊")
            self.assertEqual(journal.content, test_journal_content, "文件内容不对啊")
        except Journal.DoesNotExist:
            self.fail("没有成功更新数据库啊")

    def test_update_notes_from_md(self):
        # 每个 md 笔记的文件名类似于: "2017-02-03 任务情况总结.md"
        test_journal_title = self.test_md_file_name.rstrip(".md")  # 去掉 .md
        Journal.objects.create(title=test_journal_title, category="old_category", content="old content")

        # 文章进行了更新
        test_content = "# test_hello"
        self.__update_test_md_file_and_git_push(test_content)

        # 再次执行该视图函数, 发现数据库也跟着更新了
        self.client.get(self.unique_url)
        latest_journal = Journal.objects.get(title=test_journal_title)
        self.assertEqual(latest_journal.content, test_content, "数据库中依然是老文章的内容")

    def test_view_passes_form_to_template(self):
        """
        测试是否有将 form 传递给模板
        """
        response = self.client.get(self.unique_url)
        self.assertIsInstance(response.context["form"], JournalForm)

    def test_delete_notes_from_md(self):
        """
        原先在数据库中已经存在某个笔记, 但是最新版本的 git 仓库中并没有这个笔记, 那么从数据库中删除掉
        """
        should_not_exist_note = Journal.objects.create(title="不应该存在的笔记", category="测试笔记")

        # 确认仓库中没有这个笔记
        not_exist_note_full_name = "{}.md".format(should_not_exist_note.category)
        self.assertNotIn(not_exist_note_full_name, os.listdir(self.journals_git_path))

        # 执行视图函数
        self.client.get(self.unique_url)

        # 发现数据库中已经不存在该笔记了
        with self.assertRaises(Journal.DoesNotExist):
            Journal.objects.get(title=should_not_exist_note.title)


if __name__ == "__main__":
    pass
