#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.02.06 更换首页了, 所以对应测试也得改, 比如说现在首页不显示文章内容了
2017.02.05 添加吃饭计划表链接的按钮
2017.02.03 添加日常工作记录 app 链接的按钮
2016.10.26 添加 gitbook 链接的按钮
2016.10.03 编写功能测试, 第一个编写的功能测试测试首页各个按钮, 包括主页,about 按钮,github 按钮,archive 按钮,email 按钮
"""
from .base import FunctionalTest
from my_constant import const

import unittest
from selenium.common.exceptions import NoSuchElementException

__author__ = '__L1n__w@tch'


class TestHomePageButtons(FunctionalTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

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
        # url 没变化
        self.assertEqual(self.browser.current_url, home_page_url)

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

    @unittest.skipUnless(const.SLOW_CONNECT_DEBUG, "const.SLOW_CONNECT_DEBUG 值为 True 才表示要测试被墙的 GitHub")
    def test_github_button(self):
        # 看到 github 按钮, 点击, 发现确实跳转到了一个 github 页面上, 而且 github 页面的用户是 "L1nwatch"
        self.browser.find_element_by_id("id_github").click()
        self.assertIn("github", self.browser.current_url)
        self.assertIn("L1nwatch", self.browser.current_url)

    @unittest.skipUnless(const.SLOW_CONNECT_DEBUG, "const.SLOW_CONNECT_DEBUG 值为 True 才表示要测试被墙的 GitBook")
    def test_gitbook_button(self):
        # 看到 gitbook 按钮, 点击, 发现确实跳转到了一个 gitbook 页面上, 而且 gitbook 页面的用户是 "L1nwatch"
        self.browser.find_element_by_id("id_gitbook").click()
        self.assertIn("gitbook", self.browser.current_url)
        self.assertIn("L1nwatch".lower(), self.browser.current_url)

    def test_archive_button(self):
        # 创建测试数据
        self._create_articles_test_db_data()

        # 刷新首页
        self.browser.refresh()
        home_page_source = self.browser.page_source
        home_page_url = self.browser.current_url

        # 看到了归档按钮, 不知道有什么用, 点击看看
        self.browser.find_element_by_id("id_archives").click()

        # 发现 URL 变了
        self.assertNotEqual(self.browser.current_url, home_page_url)

        # 看见页面显示的内容跟首页不一样了
        self.assertNotEqual(self.browser.page_source, home_page_source)

        # 而且不显示文章内容
        with self.assertRaises(NoSuchElementException):
            # 如果找不到会抛出 NoSuchElementException 异常
            self.browser.find_element_by_id("id_article_content")

    def test_email_button(self):
        # Y 想联系网站拥有者, 发现了个 email 按钮
        email_button = self.browser.find_element_by_id("id_email")

        # 点击后发现页面跳转了, 而且可以看到 url 中有个 mail to 字母, 后面跟着作者的邮箱: "watch1602@gmail.com"
        # 发现如果使用 click 会使用默认浏览器打开然后就无法测试了, 所以就改用下面这种方法
        self.assertEqual("mailto:watch1602@gmail.com", email_button.get_attribute("href"))

    def test_work_journal_button(self):
        """
        2017.02.03 测试新按钮, 日常任务情况总结
        """
        # 创建测试数据
        self._create_work_journal_test_db_data()

        # Y 在首页发现了一个按钮, 日常工作笔记
        work_journal_button = self.browser.find_element_by_id("id_work_journal")

        # 点击后发现页面跳转了, URL 变化了
        home_page_url = self.browser.current_url
        work_journal_button.click()
        self.assertNotEqual(self.browser.current_url, home_page_url)

        # 而且页面显示了一堆标题, 形如: 2017-02-03 任务情况总结
        self.assertIn("2017-02-03 任务情况总结", self.browser.page_source)

        # 但是没有显示日记内容
        with self.assertRaises(NoSuchElementException):
            # 如果找不到会抛出 NoSuchElementException 异常
            self.browser.find_element_by_id("id_journal_content")

        # 不过点击标题可以链接到对应的日记, 可以看到 URL 变了
        work_journal_url = self.browser.current_url
        self.browser.find_element_by_id("id_journal").click()
        self.assertNotEqual(work_journal_url, self.browser.current_url)

        # 日记的内容也显示出来了
        self.browser.find_element_by_id("id_journal_content")

        # Y 想回到首页了, 点击首页按钮又回到了首页
        self.browser.find_element_by_id("id_home_page").click()
        self.assertEqual(self.browser.current_url, home_page_url)

    def test_eating_plan_button(self):
        """
        吃饭计划表的按钮
        """
        # Y 正在纠结吃饭的事情, 突然看到了一个吃饭计划表
        eating_plan_button = self.browser.find_element_by_id("id_just_eating")
        home_page_url = self.browser.current_url

        # Y 点击按钮, 发现页面跳转了
        eating_plan_button.click()
        self.assertNotEqual(home_page_url, self.browser.current_url)

        # 页面显示有吃货这个标题, 还有 "Home" 字样, 上面还区分了周一/周二..., 而且还区分了早/午/晚饭
        self.assertEqual("吃啥", self.browser.title)

        for each_keyword in ["Home", "周一", "周二", "周三", "周四", "周五", "周六", "周日", "早餐", "午餐", "晚餐"]:
            self.assertIn(each_keyword, self.browser.page_source)

        # Y 已经知道今晚要吃什么了, 于是点击按钮回到了首页
        self.browser.find_element_by_id("id_home_page").click()
        self.assertEqual(self.browser.current_url, home_page_url)


if __name__ == "__main__":
    pass
