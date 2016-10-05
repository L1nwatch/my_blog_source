#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""

2016.10.05 想要实现的功能, 自动获取 git 仓库上最新的笔记, 然后更新到数据库中
"""
from .base import FunctionalTest
import unittest

__author__ = '__L1n__w@tch'


class AutoUpdateDatabaseTest(FunctionalTest):
    def test_update_db_button(self):
        """
         测试更新按钮可以实现最基本的功能, 就是把 git 仓库中的笔记更新到数据库中
        :return:
        """
        # Y 访问首页, 发现首页上一篇文章都没有
        self.browser.get(self.server_url)
        self.browser.find_element_by_id()

        # 发现了一个更新数据库的按钮

        # Y 发现博主的仓库中存在笔记

        # 点击更新数据库的按钮

        # 刷新首页后可以看到博主仓库中的笔记放到了网站上了
        pass

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

    @unittest.skipIf(True, "还没开始编写")
    def test_update_db_will_delete_old_data(self):
        """
        如果 git 仓库中原本存在的某个 md 被删除了, 则数据库中对应的笔记也会删除掉
        :return:
        """
        # Y 发现博客上的某篇文章在 git 仓库中没有

        # Y 记录了一下这篇文章的名字, 然后 Y 点击更新数据库按钮

        # Y 再次搜索这篇文章, 发现已经找不到了
        pass

    @unittest.skipIf(True, "还没开始编写")
    def test_update_db_will_sync_new_data(self):
        """
        如果某篇文章已经存在, 但是 git 仓库的版本更新一些, 则数据库中对应的文章也会进行更新
        :return:
        """
        # Y 发现博客上的某篇文章跟 git 仓库的某篇文章内容不一样

        # Y 点击更新数据库按钮

        # Y 发现现在博客上的文章跟 git 仓库的文章内容一模一样了
        pass


if __name__ == "__main__":
    pass
