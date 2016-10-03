#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""

20161003 尝试编写功能测试, 第一个编写的功能测试测试首页各个按钮
"""
from .base import FunctionalTest
import unittest

__author__ = '__L1n__w@tch'


class TestHomePageButtons(FunctionalTest):
    def test_home_page_button(self):
        # Y 访问首页
        home_page_url = self.server_url
        self.browser.get(home_page_url)
        home_page_source = self.browser.page_source

        # 看到左边第一个按钮, 主页按钮, 点击进去, 没什么反应, 发现自己原来已经在首页了
        home_page_button = self.browser.find_element_by_id("id_home_page")
        home_page_button.click()
        # url 没变化, 页面内容也没变化
        self.assertEqual(self.browser.current_url, home_page_url)
        self.assertEqual(self.browser.page_source, home_page_source)

        # 点击另一个按钮, about_me 按钮, 发现界面已经变化了, 然后再点击主页按钮, 发现确实可以回到首页
        self.browser.find_element_by_id("id_about_me").click()
        # url 变化了, 页面内容也变化了
        self.assertNotEqual(self.browser.current_url, home_page_url)
        self.assertEqual(self.browser.page_source, home_page_source)

    @unittest.skipIf(True, "还没开始编写")
    def test_about_me_button(self):
        # Y 访问首页

        # 看到 about_me 按钮, 点击, 发现界面有所变化, 并且显示了作者的相关信息, 特别注意到了座右铭: "Valar Morghulis"

        pass

    @unittest.skipIf(True, "还没开始编写")
    def test_github_button(self):
        # Y 访问首页

        # 看到 github 按钮, 点击, 发现确实跳转到了一个 github 页面上, 而且 github 页面的用户是 "L1nwatch"

        pass

    @unittest.skipIf(True, "还没开始编写")
    def test_archive_button(self):
        # Y 访问首页

        # 看到了归档按钮, 不知道有什么用, 点击看看

        # 看见现在每一个文章都不会显示内容了, 而只是显示标题/时间等信息

        pass

    @unittest.skipIf(True, "还没开始编写")
    def test_email_button(self):
        # Y 访问首页

        # Y 想联系网站拥有者, 发现了个 email 按钮

        # 点击后发现页面跳转了, 而且可以看到 url 中有个 mail to 字母, 后面跟着作者的邮箱: "watch1602@gmail.com"

        pass


if __name__ == "__main__":
    pass
