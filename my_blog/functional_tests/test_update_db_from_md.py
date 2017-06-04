#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""

2017.05.01 开始实现 ajax 验证用户点击更新是否频繁的相关代码, 修正一下错误的测试代码
2016.10.05 想要实现的功能, 自动获取 git 仓库上最新的笔记, 然后更新到数据库中
"""
from .base import FunctionalTest
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException, UnexpectedAlertPresentException
from django.conf import settings
from django.test.utils import override_settings
from my_constant import const

import time
import shutil
import unittest
import os

__author__ = '__L1n__w@tch'


@override_settings(UPDATE_TIME_LIMIT=20)
@unittest.skipUnless(const.SLOW_CONNECT_DEBUG, "[*] 用户选择忽略部分测试")
class AutoUpdateDatabaseTest(FunctionalTest):
    def setUp(self):
        super().setUp()

        self.test_url = "{host}/{path}"

        # Y 访问归档页
        self.browser.get(self.test_url.format(host=self.server_url, path="articles/archives/"))

    def test_update_notes_button(self):
        """
         测试更新按钮可以实现最基本的功能, 就是把 git 仓库中的笔记更新到数据库中
        :return:
        """
        try:
            # Y 发现归档页上一篇文章都没有
            self.browser.find_element_by_id("id_article_title")
        except NoSuchElementException:
            # Y 发现博主的仓库中存在笔记
            if self.__git_repo_has_notes():
                # 同时 Y 发现了一个更新数据库 url, 访问它
                self.browser.get(self.test_url.format(host=self.server_url, path="articles/update_notes/"))

                # 归档页上终于能看到文章了
                try:
                    self.browser.find_element_by_id("id_article_title")
                except NoSuchElementException:
                    self.fail("更新按钮没有起作用, 首页依然没有文章")
            else:
                self.fail("笔记仓库中没数据没法测试啊")

    @staticmethod
    def __git_repo_has_notes():
        # TODO: 还没实现
        return True

    def test_can_not_continue_click_update_db_button(self):
        """
        防止恶意点击更新数据库导致后台一直运行, 相邻两次点击之间存在时间间隔
        """
        # Y 想当一个坏人, 试图利用更新数据库的按钮就进行 dos 攻击
        # Y 连续点击了 10 次更新数据库按钮
        with self.assertRaises(UnexpectedAlertPresentException) as e:
            for i in range(10):
                update_note_button = self.browser.find_element_by_id("id_update_notes")
                update_note_button.click()

        self.assertIn("text: [-] 操作频繁, 现在无法执行更新操作", str(e.exception))

        # Y 等待 UPDATE_TIME_LIMIT s 后再次点击, 发现没有弹出窗口了
        time.sleep(settings.UPDATE_TIME_LIMIT + 5)
        update_note_button = self.browser.find_element_by_id("id_update_notes")
        update_note_button.click()

        # 验证没有弹出窗口
        with self.assertRaises(NoAlertPresentException):
            message = self.browser.switch_to_alert()
            self.assertEqual(message.text, "[-] 操作频繁, 现在无法执行更新操作")
            self.browser.switch_to_alert().accept()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        if os.path.exists(const.NOTES_GIT_PATH):
            shutil.rmtree(const.NOTES_GIT_PATH)


if __name__ == "__main__":
    pass
