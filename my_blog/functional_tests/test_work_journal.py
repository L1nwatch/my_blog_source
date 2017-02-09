#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.02.08 新增搜索功能, 编写功能测试
2017.02.05 为这个 APP 建立一个单独的功能测试文件
"""
from .base import FunctionalTest
from my_constant import const

__author__ = '__L1n__w@tch'


class TestWorkJournalHomePage(FunctionalTest):
    unique_url = "/work_journal/"

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_display_journal_numbers(self):
        """
        测试左下角显示的数字
        """
        # Y 打开了 work_journal 首页
        self.browser.get("{host}{path}".format(host=self.server_url, path=self.unique_url))

        # Y 发现左下角有个日记数, 且日记数不为 0, 说明站长是有记日记的
        self.assertIn("日记数", self.browser.page_source)
        self.assertRegex(self.browser.page_source, "日记数: \d+")


class TestWorkJournalSearch(FunctionalTest):
    unique_url = "/work_journal/"

    def setUp(self):
        super().setUp()
        self.work_journal_home = "{host}{path}".format(host=self.server_url, path=self.unique_url)
        self._create_work_journal_test_db_data()

        # Y 打开日记的首页
        self.browser.get(self.work_journal_home)

        # Y 看到一堆乱七八糟的日期标题
        self.assertRegex(self.browser.page_source, "2017-02-08.*")
        self.assertRegex(self.browser.page_source, "2017-02-07.*")
        self.assertRegex(self.browser.page_source, "2017-02-09.*")

    def test_can_search_by_date(self):
        # Y 决定试试左边的搜索功能, 搜索指定的日期
        search_button = self.browser.find_element_by_id("id_search_work_journal")
        search_button.send_keys("2017-02-08\n")

        # Y 发现搜索结果中只有一篇, 而且是刚才自己搜索的日期
        self.assertRegex(self.browser.page_source, "2017-02-08[^\"]+")  # 注意区分搜索框里的值
        self.assertNotRegex(self.browser.page_source, "2017-02-07.+")
        self.assertNotRegex(self.browser.page_source, "2017-02-09.+")

    def test_can_search_by_content(self):
        # Y 怀疑是不是只能搜索日期不能靠内容来搜索, 于是搜索指定内容
        search_button = self.browser.find_element_by_id("id_search_work_journal")
        search_button.send_keys("python\n")

        # 发现了有文章被搜索出来, 搜索结果标题里面没有刚才搜索的内容
        self.assertNotIn("python", self.browser.find_element_by_id(const.ID_SEARCH_RESULT_TITLE).text.lower())

        # Y 打开搜索出来的文章, 发现自己搜索的内容确实存在于文章之中
        self.browser.find_element_by_id(const.ID_SEARCH_RESULT_TITLE).click()
        self.assertIn("python", self.browser.page_source.lower())

    def test_can_search_without_case(self):
        # Y 知道有篇文章提到了 Python, 但是 Y 故意输入大小写混乱的 pYthOn 想看下能否搜出来
        search_button = self.browser.find_element_by_id("id_search_work_journal")
        search_button.send_keys("pYthOn\n")

        # 发现确实能搜索出来, 而且打开文章内容, python 确实存在
        self.browser.find_element_by_id(const.ID_SEARCH_RESULT_TITLE).click()
        self.assertIn("python", self.browser.page_source.lower())

    def test_can_search_multi_keyword(self):
        # Y 想知道这个支不支持多个关键词搜索, 于是搜索了 python test
        search_button = self.browser.find_element_by_id("id_search_work_journal")
        search_button.send_keys("python test\n")

        # 发现有结果出来
        self.browser.find_element_by_id(const.ID_SEARCH_RESULT_TITLE).click()

        # 打开日记一看, python 和 test 都存在, 而且这两个关键词并不是连在一起的
        self.assertIn("python", self.browser.page_source.lower())
        self.assertIn("test", self.browser.page_source.lower())
        self.assertNotIn("python test", self.browser.page_source.lower())

    def test_search_result_display(self):
        """
        搜索结果不应该只包含对应的日记标题, 还应该有对应的内容
        """
        # Y 知道某篇日记含有 python 这个关键词, 于是搜索看看
        search_button = self.browser.find_element_by_id("id_search_work_journal")

        # Y 知道日记所在行内容为 <# Test pyThon>
        # 于是 Y 搜索 markdown1, 看是否显示这篇文章及结果出来
        search_button.send_keys("python\n")

        # 搜索结果出来了, Y 看到了自己搜索的关键词
        search_keyword = self.browser.find_element_by_id("id_search_work_journal").get_attribute("value")
        self.assertEqual(search_keyword, "python")

        # Y 查看搜索结果, 发现其找到对应文章了
        search_result = self.browser.find_element_by_tag_name("body").text
        self.assertIn("2017-02-08 任务情况总结", search_result)

        # 显示对应搜索结果
        self.assertIn("Test pyThon", search_result)

    def test_only_search_journals(self):
        """
        日记 APP 的搜索功能只支持搜索日记, 不会去搜索文章
        """
        self._create_articles_test_db_data()
        # Y 知道某篇文章及某篇日记都有 python 这个关键词, 于是 Y 打算试试搜索结果是否都能搜索出来
        search_button = self.browser.find_element_by_id("id_search_work_journal")
        search_button.send_keys("python\n")

        # Y 知道存在这个关键字的日记所在行内容为 <# Test pyThon>, 日记标题为 <2017-02-08 任务情况总结>
        # Y 也知道存在这个关键字的文章标题为 <article_with_python>, 所在行内容为 <I am `Python`>

        # Y 只看到了日记
        search_result = self.browser.find_element_by_tag_name("body").text
        self.assertIn("2017-02-08 任务情况总结", search_result)
        self.assertIn("Test pyThon", search_result)

        # Y 没看到对应的文章
        search_result = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("I am Python", search_result)
        self.assertNotIn("article_with_python", search_result)


if __name__ == "__main__":
    pass
