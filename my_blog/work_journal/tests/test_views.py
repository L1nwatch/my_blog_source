#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.03.23 重构了部分搜索实现, 删除了通过 URL 来区分搜索类型的相关代码
2017.03.17 重构一下测试用的 md 文件的路径
2017.02.08 测试提取日期对象的方法
2017.02.07 添加更新的时候判断文件名的合法性的单元测试
2017.02.03 开始写这个 APP, 需要新建单元测试
"""
import unittest
import shutil
import os
import datetime

from work_journal.forms import JournalForm, BaseSearchForm
from work_journal.models import Journal
from work_journal.views import is_valid_update_md_file, extract_date_from_md_file
from articles.views import get_right_content_from_file
from my_constant import const
from django.test import TestCase, override_settings
from django.conf import settings

__author__ = '__L1n__w@tch'


class BaseCommonTest(TestCase):
    @staticmethod
    def create_journal_test_db():
        """
        创建测试用的日记数据
        """
        today = datetime.datetime.today()
        tomorrow = today + datetime.timedelta(days=1)

        # 创建一篇普通的日记
        Journal.objects.create(title="test_journal_1", content="test_journal_content_1",
                               date=today)

        # 创建一篇 Markdown 格式的日记
        with open(os.path.join(settings.BASE_DIR, "articles", "tests", "markdown_file_for_test.md"), "r") as f:
            content = f.read()

        Journal.objects.create(title="test_journal_with_markdown", content=content, date=tomorrow)


class JournalHomeViewTest(TestCase):
    unique_url = "/work_journal/"

    @staticmethod
    def _create_test_db_date():
        journal = Journal.objects.create(title="test_journal_1", content="test_journal_content_1"
                                         , date=datetime.datetime.today())

        return journal

    def test_view_passes_form_to_template(self):
        """
        测试是否有将 form 传递给模板
        """
        response = self.client.get(self.unique_url)
        self.assertIsInstance(response.context["form"], JournalForm)

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
        self.assertContains(response, 'name="search_content"')

    def test_display_no_journals(self):
        """
        2017.02.13 首页换了, 现在一篇日记都不显示
        测试显示了所有 journal 而不只是某几篇
        """
        test_journals_number = 10
        test_date = datetime.datetime.today()

        # 测试 10 篇文章
        for i in range(test_journals_number):
            Journal.objects.create(title="test_journal_{}".format(i + 1), date=test_date)
            test_date += datetime.timedelta(days=1)

        response = self.client.get(self.unique_url)
        counts = 0
        for journal in Journal.objects.all():
            journal_url = "{}{}/".format(self.unique_url, journal.id)
            if journal_url.encode("utf8") in response.content:
                counts += 1
        self.assertNotEqual(counts, test_journals_number)

    def test_no_display_journal_content(self):
        """
        测试日常汇总首页不显示日记的内容
        """
        journal = self._create_test_db_date()

        response = self.client.get(self.unique_url)
        self.assertNotContains(response, journal.content)


class JournalDisplayViewTest(BaseCommonTest):
    unique_url = "/work_journal/{}/"

    def setUp(self):
        super().__init__()

        self.create_journal_test_db()

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


class HelpFunctionTest(TestCase):
    def test_is_valid_update_md_file(self):
        test_file_name = "readme.md"
        self.assertFalse(is_valid_update_md_file(test_file_name))

        test_file_name = "添加路由的命令.md"
        self.assertFalse(is_valid_update_md_file(test_file_name))

        test_file_name = "【路由部署】关键字编写实战.md"
        self.assertFalse(is_valid_update_md_file(test_file_name))

        test_file_name = "notes_id导入问题.md"
        self.assertFalse(is_valid_update_md_file(test_file_name))

        test_file_name = "ftp爆破.png"
        self.assertFalse(is_valid_update_md_file(test_file_name))

        # 以下为符合要求的情况
        test_file_name = "20161130任务情况总结.md"
        self.assertTrue(is_valid_update_md_file(test_file_name))

        test_file_name = "2016-12-12-周一.md"
        self.assertTrue(is_valid_update_md_file(test_file_name))

    def test_extract_date_from_md_file(self):
        test_file_name = "20161130任务情况总结.md"
        right_answer = datetime.date(2016, 11, 30)
        my_answer = extract_date_from_md_file(test_file_name)
        self.assertEqual(my_answer, right_answer)

        test_file_name = "2016-12-12-周一.md"
        right_answer = datetime.date(2016, 12, 12)
        my_answer = extract_date_from_md_file(test_file_name)
        self.assertEqual(my_answer, right_answer)

        test_file_name = "2016-12-1-周一.md"
        right_answer = datetime.date(2016, 12, 1)
        my_answer = extract_date_from_md_file(test_file_name)
        self.assertEqual(my_answer, right_answer)


class JournalSearchViewTest(BaseCommonTest):
    unique_url = "/search/"

    def test_use_right_template_to_show_search_result(self):
        """
        日记搜索用的模板应该和 articles APP 用的一样
        """
        response = self.client.post(self.unique_url, data={"search_content": "随便输入了一些什么",
                                                           "search_choice": "journals"})
        self.assertTemplateUsed(response, "search_result.html")

    def test_search_result_display(self):
        """
        测试搜索出来能够显示日记的标题和结果
        """
        self.create_journal_test_db()

        journal = Journal.objects.get(title="test_journal_1")
        response = self.client.post(self.unique_url, data={"search_content": journal.content,
                                                           "search_choice": "journals"})
        self.assertContains(response, journal.title)
        self.assertContains(response, journal.content)

    def test_journal_href_right(self):
        """
        测试搜索出来的日记链接正确
        """
        self.create_journal_test_db()

        journal = Journal.objects.get(title="test_journal_1")
        response = self.client.post(self.unique_url, data={"search_content": journal.content,
                                                           "search_choice": "journals"})

        self.assertContains(response, "/work_journal/{}/".format(journal.id))

    def test_search_multiple_keywords(self):
        """
        测试同时搜索多个关键词, 能搜索出来结果
        """
        self.create_journal_test_db()

        # 日记 <test_journal_1> 里面有单词 <journal> <content>, 所在行为 <test_journal_content_1>
        journal = Journal.objects.get(title="test_journal_1")
        response = self.client.post(self.unique_url, data={"search_content": "conTent journal",
                                                           "search_choice": "journals"})

        self.assertContains(response, journal.title)

    def test_search_date_right(self):
        """
        测试能够通过搜索日期来得到对应的日记
        """
        self.create_journal_test_db()

        journal = Journal.objects.get(title="test_journal_1")

        # 测试只搜年, 搜不到
        response = self.client.post(self.unique_url, data={"search_content": "{}".format(journal.date.year),
                                                           "search_choice": "journals"})
        self.assertNotContains(response, journal.title)

        # 测试只搜年和月, 搜不到
        response = self.client.post(self.unique_url,
                                    data={"search_content": "{}-{}".format(journal.date.year, journal.date.month),
                                          "search_choice": "journals"})
        self.assertNotContains(response, journal.title)

        # 测试搜年-月-日, 可以搜到
        response = self.client.post(self.unique_url,
                                    data={"search_content": "{}-{}-{}".format(journal.date.year,
                                                                              journal.date.month,
                                                                              journal.date.day),
                                          "search_choice": "journals"})
        self.assertContains(response, journal.title)

    def test_search_no_exist_date_journal(self):
        """
        搜索不存在日记的日期时, 应该跑去 404 页面
        """
        today = datetime.datetime.today()

        response = self.client.post(self.unique_url, data={"search_content": "{}-{}-{}".format(today.year,
                                                                                               today.month,
                                                                                               today.day),
                                                           "search_choice": "journals"})
        self.assertContains(response, const.EMPTY_ARTICLE_ERROR)


@override_settings(UPDATE_TIME_LIMIT=0.1)
@unittest.skipUnless(const.SLOW_CONNECT_DEBUG, "[*] 用户选择忽略部分测试")
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

    @classmethod
    def tearDownClass(cls):
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

    def test_update_empty_md(self):
        """
        测试如果下载到的是空的 md 文件, 则不会写入到数据库中
        """
        journal_title = self.test_md_file_name.split(".md")[0]

        # 原来存在这份笔记
        Journal.objects.create(title=journal_title, content="测试笔记", date=datetime.date.today())

        # 将测试文件的内容更改为空并且 git 上去
        test_content = ""
        self.__update_test_md_file_and_git_push(test_content)

        # 执行更新操作
        self.client.get(self.unique_url)

        # 发现数据库中不存在这份笔记
        with self.assertRaises(Journal.DoesNotExist):
            Journal.objects.get(title=journal_title)

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
        Journal.objects.create(title=test_journal_title, category="old_category",
                               content="old content", date=datetime.date.today())

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
        should_not_exist_note = Journal.objects.create(title="不应该存在的笔记",
                                                       category="测试笔记", date=datetime.date.today())

        # 确认仓库中没有这个笔记
        not_exist_note_full_name = "{}.md".format(should_not_exist_note.category)
        self.assertNotIn(not_exist_note_full_name, os.listdir(self.journals_git_path))

        # 执行视图函数
        self.client.get(self.unique_url)

        # 发现数据库中已经不存在该笔记了
        with self.assertRaises(Journal.DoesNotExist):
            Journal.objects.get(title=should_not_exist_note.title)


class RedirectViewTest(BaseCommonTest):
    unique_url = "/work_journal/{}/"

    def setUp(self):
        super().setUp()

        self.create_journal_test_db()

    def test_use_right_template(self):
        """
        测试这个跳转页面, 最终应该跳转到显示日记的那个 html
        """
        # 正常情况下
        today = datetime.datetime.today()
        response = self.client.get(self.unique_url.format("{}-{}-{}".format(today.year, today.month, today.day)))
        self.assertTemplateUsed(response, "journal_display.html")

        # 非正常情况下, 应该是会去 404 页面
        not_exist_day = datetime.datetime(1994, 4, 6)
        response = self.client.get(self.unique_url.format("{}-{}-{}".format(not_exist_day.year,
                                                                            not_exist_day.month,
                                                                            not_exist_day.day)))
        self.assertTemplateUsed(response, "journal_not_found.html")

    def test_redirect_right(self):
        """
        测试几种 url 都能够正确解析
        """
        # 类似于 2017-02-13 的 url
        test_journal = Journal.objects.create(title="2017-02-13 任务情况", date=datetime.datetime(2017, 2, 13))
        response = self.client.get(self.unique_url.format("2017-02-13"))
        self.assertContains(response, test_journal.title)

        # 类似于 2017-2-13 的 url
        response = self.client.get(self.unique_url.format("2017-2-13"))
        self.assertContains(response, test_journal.title)

        # 类似于 2016-12-03 的 url
        test_journal = Journal.objects.create(title="test2", date=datetime.datetime(2016, 12, 3))
        response = self.client.get(self.unique_url.format("2016-12-03"))
        self.assertContains(response, test_journal.title)

        # 类似于 2016-12-3 的 url
        response = self.client.get(self.unique_url.format("2016-12-3"))
        self.assertContains(response, test_journal.title)

    def test_404_redirect(self):
        """
        测试查询一篇不存在的日记时是否会跳转到 404 页面
        """
        not_exist_day = datetime.datetime(1994, 4, 6)
        response = self.client.get(self.unique_url.format("{}-{}-{}".format(not_exist_day.year,
                                                                            not_exist_day.month,
                                                                            not_exist_day.day)))
        # 查看一下页面是否有站长预先留下的信息提示
        self.assertContains(response, const.JOURNAL_NOT_FOUND)

    def test_404_form(self):
        """
        404 页面也有搜索功能, 所以需要表单验证
        """
        response = self.client.get(self.unique_url.format("1994-04-06"))
        self.assertIsInstance(response.context["form"], JournalForm)


if __name__ == "__main__":
    pass
