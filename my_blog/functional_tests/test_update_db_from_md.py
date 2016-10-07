#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""

2016.10.05 想要实现的功能, 自动获取 git 仓库上最新的笔记, 然后更新到数据库中
"""
from .base import FunctionalTest
from selenium.common.exceptions import NoSuchElementException
from django.conf import settings
import unittest

__author__ = '__L1n__w@tch'

TEST_GIT_REPOSITORY = settings.TEST_GIT_REPOSITORY


class AutoUpdateDatabaseTest(FunctionalTest):
    def test_update_notes_button(self):
        """
         测试更新按钮可以实现最基本的功能, 就是把 git 仓库中的笔记更新到数据库中
        :return:
        """
        # Y 访问首页
        self.browser.get(self.server_url)

        # 发现首页上一篇文章都没有
        try:
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

    @unittest.skipIf(True, "还没开始编写")
    def test_can_not_continue_click_update_db_button(self):
        """
        防止恶意点击更新数据库导致后台一直运行, 相邻两次点击之间存在时间间隔
        :return:
        """
        # Y 想当一个坏人, 试图利用更新数据库的按钮就进行 dos 攻击

        # Y 点击了第一次更新数据库按钮

        # 紧接着 Y 又点击了第二次

        # 但是发现网站弹出了个提示, 说是一定时间内不允许再次更新数据库了
        pass


if __name__ == "__main__":
    pass
