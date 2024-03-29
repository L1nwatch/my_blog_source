#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.12.03 解决点击失败的问题
2017.06.29 给首页新增一个 timeline 的按钮
2017.06.06 重构, 将有关 archive 的测试分离出来
2017.06.04 重构基类测试, 修改对应代码
2017.03.28 修改 about me 的测试
2017.03.24 新增一个 tool_hub APP, 于是编写相关测试
2017.02.13 日记更换首页了, 对应的测试得修改下
2017.02.06 更换首页了, 所以对应测试也得改, 比如说现在首页不显示文章内容了
2017.02.05 添加吃饭计划表链接的按钮
2017.02.03 添加日常工作记录 app 链接的按钮
2016.10.26 添加 gitbook 链接的按钮
2016.10.03 编写功能测试, 第一个编写的功能测试测试首页各个按钮, 包括主页,about 按钮,github 按钮,archive 按钮,email 按钮
"""
# 标准库
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

import unittest
import datetime

# 自己的
from .base import FunctionalTest
import my_constant as const

__author__ = '__L1n__w@tch'


class TestHomePageButtons(FunctionalTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        super().setUp()
        # Y 访问首页
        self.browser.get(self.app_articels_url)

    def test_home_page_button(self):
        home_page_url = self.browser.current_url
        home_page_source = self.browser.page_source

        # 发现页面有个 about_me 按钮,试着点一下
        about_me_button = self.browser.find_element(By.ID, "id_about_me")
        self.move_and_click(about_me_button)

        # 发现 url 变化了, 页面内容也变化了
        self.assertNotEqual(self.browser.current_url, home_page_url)
        self.assertNotEqual(self.browser.page_source, home_page_source)

        # 回到首页, 想试试其他按钮
        self.browser.back()

        # 看到左边第一个按钮, 主页按钮, 点击进去, 没什么反应, 发现自己原来已经在首页了
        home_page_button = self.browser.find_element(By.ID, "id_home_page")
        self.move_and_click(home_page_button)

        # url 没变化
        self.assertEqual(self.browser.current_url, home_page_url)

    def test_about_me_button(self):
        """
        2017.03.28 about me 是由 Pages 创建的, 所以测试不太方便, 这里修改成仅测试能否打开 about me 页面
        """
        home_page_source = self.browser.page_source

        # 看到 about_me 按钮, 点击, 发现界面有所变化, 看上去像是一份简历, 由 Pages 生成的
        about_me_button = self.browser.find_element(By.ID, "id_about_me")
        self.move_and_click(about_me_button)
        self.assertNotEqual(self.browser.page_source, home_page_source)

    @unittest.skipUnless(const.SLOW_CONNECT_DEBUG, "[*] 用户选择忽略部分测试")
    def test_github_button(self):
        # 看到 github 按钮, 点击, 发现确实跳转到了一个 github 页面上, 而且 github 页面的用户是 "L1nwatch"
        self.browser.find_element(By.ID, "id_github").click()
        self.assertIn("github", self.browser.current_url)
        self.assertIn("L1nwatch", self.browser.current_url)

    @unittest.skipUnless(const.SLOW_CONNECT_DEBUG, "[*] 用户选择忽略部分测试")
    def test_gitbook_button(self):
        # 看到 gitbook 按钮, 点击, 发现确实跳转到了一个 gitbook 页面上, 而且 gitbook 页面的用户是 "L1nwatch"
        self.browser.find_element(By.ID, "id_gitbook").click()
        self.assertIn("gitbook", self.browser.current_url)
        self.assertIn("L1nwatch".lower(), self.browser.current_url)

    def test_email_button(self):
        # Y 想联系网站拥有者, 发现了个 email 按钮
        email_button = self.browser.find_element(By.ID, "id_email")

        # 点击后发现页面跳转了, 而且可以看到 url 中有个 mail to 字母, 后面跟着作者的邮箱: "watch1602@gmail.com"
        # 发现如果使用 click 会使用默认浏览器打开然后就无法测试了, 所以就改用下面这种方法
        self.assertEqual("mailto:watch1602@gmail.com", email_button.get_attribute("href"))

    def test_work_journal_button(self):
        """
        2017.02.13 将首页换成万年历, 因此不会显示日记了
        2017.02.03 测试新按钮, 日常任务情况总结
        """
        today = datetime.datetime.today()
        # 创建测试数据
        self.create_work_journal_test_db_data()

        # Y 在首页发现了一个按钮, 日常工作笔记
        work_journal_button = self.browser.find_element(By.ID, "id_work_journal")

        # 点击后发现页面跳转了, URL 变化了
        home_page_url = self.browser.current_url
        work_journal_button.click()
        self.assertNotEqual(self.browser.current_url, home_page_url)

        # 而且页面显示了一堆标题, 而且还显示了今天的日期
        self.assertIn("{}-{}-{}".format(today.year, today.month, today.day), self.browser.page_source)

        # 但是没有显示日记内容
        with self.assertRaises(NoSuchElementException):
            # 如果找不到会抛出 NoSuchElementException 异常
            self.browser.find_element(By.ID, "id_journal_content")

        # Y 想回到首页了, 点击首页按钮又回到了首页
        self.browser.find_element(By.ID, "id_home_page").click()
        self.assertEqual(self.browser.current_url.strip("/"), self.index_url)

    def test_eating_plan_button(self):
        """
        吃饭计划表的按钮
        """
        # Y 正在纠结吃饭的事情, 突然看到了一个吃饭计划表
        eating_plan_button = self.browser.find_element(By.ID, "id_just_eating")
        home_page_url = self.browser.current_url

        # Y 点击按钮, 发现页面跳转了
        eating_plan_button.click()
        self.assertNotEqual(home_page_url, self.browser.current_url)

        # 页面显示有吃货这个标题, 还有 "Home" 字样, 上面还区分了周一/周二..., 而且还区分了早/午/晚饭
        self.assertEqual("吃啥", self.browser.title)

        for each_keyword in ["Home", "周一", "周二", "周三", "周四", "周五", "周六", "周日", "早餐", "午餐", "晚餐"]:
            self.assertIn(each_keyword, self.browser.page_source)

        # Y 已经知道今晚要吃什么了, 于是点击按钮回到了首页
        self.browser.find_element(By.ID, "id_home_page").click()
        self.assertEqual(self.browser.current_url, home_page_url)

    def test_toolhub_button(self):
        """
        2017.03.24 新增一个 tool_hub APP
        """
        # Y 打开首页, 发现右上角多出了一个 tool_hub 的按钮
        home_url = self.browser.current_url
        toolhub_button = self.browser.find_element(By.ID, "id_toolhub")

        # 点击一下
        toolhub_button.click()

        # 发现页面上显示了很多工具名称, 比如其中一个名称是: GitHub 图片地址转换
        self.assertIn("GitHub 图片地址转换", self.browser.page_source)

        # Y 知道这个 APP 是干啥的了, 于是点击返回首页按钮回到首页了
        home_button = self.browser.find_element(By.ID, "id_home_page")
        home_button.click()
        self.assertEqual(self.browser.current_url, home_url)

    def test_timeline_button(self):
        """
        测试首页上的 timeline 按钮
        """
        # Y 打开首页, 发现右下角多出了一个 timeline 的按钮, 图标是一个 clock
        home_url = self.browser.current_url
        timeline_button = self.browser.find_element(By.ID, "id_timeline")

        # Y 想看一下这个按钮会显示啥东西, 于是点击了一下
        self.move_and_click(timeline_button)

        # Y 发现界面的 URL 发生了变化, 而且界面上出现了一堆时间信息, 比如 2017.06.28
        self.assertNotEqual(self.browser.current_url, home_url)
        self.assertTrue(r'<span class="day">28</span>' in self.browser.page_source)
        self.assertTrue(r'<div class="year"><h2>2017</h2>' in self.browser.page_source)
        self.assertTrue(r'<span class="month">July</span>' in self.browser.page_source)

        # Y 看完了所有时间事件, 于是点击返回回到了首页
        home_button = self.browser.find_element(By.ID, "id_home_page")
        home_button.click()
        self.assertEqual(self.browser.current_url, home_url)

    def test_life_summary_button(self):
        """
        测试首页上的 life_summary 按钮
        """
        # Y 打开首页, 发现右下角多出了一个 life_summary 的按钮, 图标是一个 Note
        home_url = self.browser.current_url
        # timeline_button = self.browser.find_element(By.ID, "id_life_summary")
        action = ActionChains(self.browser)
        timeline_button = self.browser.find_element(By.ID, "id_life_summary")

        # Y 想看一下这个按钮会显示啥东西, 于是点击了一下
        action.move_to_element(timeline_button).click(timeline_button).perform()

        # Y 发现界面的 URL 发生了变化, 而且界面上出现了个人经历, 比如 xxxx
        self.assertNotEqual(self.browser.current_url, home_url)
        self.assertTrue(r'<div>洗漱用品</div>' in self.browser.page_source)
        self.assertTrue(r'<div>生活习惯</div>' in self.browser.page_source)

        # Y 看完了, 于是点击返回回到了首页
        home_button = self.browser.find_element(By.ID, "id_home_page")
        action = ActionChains(self.browser)
        action.move_to_element(home_button)
        home_button.click()

        self.assertEqual(self.browser.current_url.strip("/"), self.index_url)
