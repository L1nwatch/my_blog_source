#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.02.05 为这个 APP 建立一个单独的功能测试文件
"""
from .base import FunctionalTest

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


if __name__ == "__main__":
    pass
