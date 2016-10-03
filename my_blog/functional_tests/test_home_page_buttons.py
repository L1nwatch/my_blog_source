#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""

2016.10.03 编写功能测试, 第一个编写的功能测试测试首页各个按钮, 包括主页,about 按钮,github 按钮,archive 按钮,email 按钮
"""
from .base import FunctionalTest
import unittest

__author__ = '__L1n__w@tch'


class TestHomePageButtons(FunctionalTest):
    def setUp(self):
        super().setUp()
        # Y 访问首页
        self.browser.get(self.server_url)

    def test_home_page_button(self):
        home_page_url = self.browser.current_url
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
        self.assertNotEqual(self.browser.page_source, home_page_source)

    def test_about_me_button(self):
        home_page_source = self.browser.page_source

        # 看到 about_me 按钮, 点击, 发现界面有所变化, 并且显示了作者的相关信息, 特别注意到了座右铭: "Valar Morghulis"
        self.browser.find_element_by_id("id_about_me").click()
        self.assertNotEqual(self.browser.page_source, home_page_source)
        table = self.browser.find_element_by_id("id_information_list")
        rows = table.find_elements_by_tag_name("tr")
        self.assertIn(r"座右铭: Valar Morghulis", [row.text for row in rows])

    def test_github_button(self):
        # 看到 github 按钮, 点击, 发现确实跳转到了一个 github 页面上, 而且 github 页面的用户是 "L1nwatch"
        self.browser.find_element_by_id("id_github").click()
        self.assertIn("github", self.browser.current_url)
        self.assertIn("L1nwatch", self.browser.current_url)

    @unittest.skipIf(True, "还没开始编写")
    def test_archive_button(self):
        home_page_source = self.browser.page_source

        # 看到了归档按钮, 不知道有什么用, 点击看看
        self.browser.find_element_by_id("id_archive").click()

        # 看见现在每一个文章都不会显示内容了, 而只是显示标题/时间等信息
        self.assertNotEqual(self.browser.page_source, home_page_source)

        pass

    def test_email_button(self):
        # Y 想联系网站拥有者, 发现了个 email 按钮
        email_button = self.browser.find_element_by_id("id_email")

        # 点击后发现页面跳转了, 而且可以看到 url 中有个 mail to 字母, 后面跟着作者的邮箱: "watch1602@gmail.com"
        # 发现如果使用 click 会使用默认浏览器打开然后就无法测试了, 所以就改用下面这种方法
        self.assertEqual("mailto:watch1602@gmail.com", email_button.get_attribute("href"))

if __name__ == "__main__":
    pass
