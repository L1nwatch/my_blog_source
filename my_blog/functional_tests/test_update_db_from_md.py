#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""

2016.10.05 想要实现的功能, 自动获取 git 仓库上最新的笔记, 然后更新到数据库中
"""
from .base import FunctionalTest
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException
from django.conf import settings
from django.test.utils import override_settings
from my_constant import const

import time
import unittest

__author__ = '__L1n__w@tch'


@override_settings(UPDATE_TIME_LIMIT=5)
@unittest.skipUnless(const.SLOW_CONNECT_DEBUG, "const.SLOW_CONNECT_DEBUG 值为 True 才表示要进行 git 测试")
class AutoUpdateDatabaseTest(FunctionalTest):
    def setUp(self):
        super().setUp()

        # 休息 UPDATE_TIME_LIMIT 时间
        time.sleep(settings.UPDATE_TIME_LIMIT)

        # Y 访问首页
        self.browser.get(self.server_url)

    def test_update_notes_button(self):
        """
         测试更新按钮可以实现最基本的功能, 就是把 git 仓库中的笔记更新到数据库中
        :return:
        """
        try:
            # Y 发现首页上一篇文章都没有
            self.browser.find_element_by_id("id_article_title")
        except NoSuchElementException:
            # Y 发现博主的仓库中存在笔记
            if self.__git_repo_has_notes():
                # 同时 Y 发现了一个更新数据库的按钮, 点击
                self.browser.find_element_by_id("id_update_notes").click()

                # Y 发现首页刷新了(下面这一条多余了)
                self.browser.refresh()

                # 首页上终于能看到文章了
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

    # TODO: 暂时没办法通过这个测试
    @unittest.skipIf(True, "等学了 ajax 才能通过这个功能测试吧")
    def test_can_not_continue_click_update_db_button(self):
        """
        防止恶意点击更新数据库导致后台一直运行, 相邻两次点击之间存在时间间隔
        :return:
        """
        # Y 访问首页
        self.browser.get(self.server_url)

        # Y 想当一个坏人, 试图利用更新数据库的按钮就进行 dos 攻击
        update_note_button = self.browser.find_element_by_id("id_update_notes")

        # Y 点击了第一次更新数据库按钮
        update_note_button.click()

        # 紧接着 Y 又点击了第二次
        update_note_button = self.browser.find_element_by_id("id_update_notes")
        update_note_button.click()

        # 但是发现网站弹出了个提示, 说是操作频繁, 于是只好点击确认
        message = self.browser.switch_to_alert()
        self.assertEqual(message.text, "操作频繁")
        self.browser.switch_to_alert().accept()

        # Y 等待 UPDATE_TIME_LIMIT s 后再次点击, 发现没有弹出窗口了
        time.sleep(settings.UPDATE_TIME_LIMIT + 5)
        update_note_button = self.browser.find_element_by_id("id_update_notes")
        update_note_button.click()
        with self.assertRaises(NoAlertPresentException):
            self.browser.switch_to_alert()


if __name__ == "__main__":
    pass
