#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.03.22 添加一个转盘网页, 实现随机选择备选菜单的功能, 于是新增对应测试
2017.02.26 开始更新在学校的吃饭菜单
"""
import re

from .base import FunctionalTest

__author__ = '__L1n__w@tch'


class JustEatingHomeViewTest(FunctionalTest):
    def setUp(self):
        super().setUp()
        self.test_url = "{host}/{path}".format(host=self.server_url, path="just_eating/")

        # Y 访问吃饭的首页
        self.browser.get(self.test_url)

    def test_home_view_display(self):
        """
        首页只显示 home 的吃饭菜单, 不显示 school 的吃饭菜单
        """
        # Y 发现首页上显示了 Home 吃饭的菜单
        home_eating_re = re.compile("Home.*Eating")

        self.assertRegex(self.browser.page_source, home_eating_re)

        # Y 没有发现在 School 吃饭的菜单
        school_eating_re = re.compile("School.*Eating")
        self.assertNotRegex(self.browser.page_source, school_eating_re)

    def test_web_home_button(self):
        """
        测试返回到网站首页的按钮
        """
        # Y 发现首页上有个 web home 按钮, 点击一下
        home_url = self.browser.current_url
        self.browser.find_element_by_id("id_home_page").click()

        # Y 发现回到了网站首页了
        self.assertNotRegex(self.browser.current_url, home_url)
        self.assertRegex(self.browser.current_url, self.server_url)

    def test_home_school_eating_buttons(self):
        """
        测试链接到 Home 吃饭的按钮
        """
        # Y 发现首页上还有一个 Home 按钮, 点击一下
        home_url = self.browser.current_url
        home_eating_button = self.browser.find_element_by_id("id_home_eating").click()

        # Y 没发现什么变化, URL 也就多了一串 "home" 字眼
        self.assertNotEqual(home_url, self.browser.current_url)
        self.assertRegex(self.browser.current_url, "home")
        home_url = self.browser.current_url

        # Y 点击了 School 按钮
        school_eating_button = self.browser.find_element_by_id("id_school_eating").click()

        # 发现页面变化了, 不显示 Home 菜单而是显示 School 菜单
        school_eating_re = re.compile("School.*Eating", flags=re.IGNORECASE)
        self.assertRegex(self.browser.page_source, school_eating_re)
        self.assertNotEqual(home_url, self.browser.current_url)

        # Y 再次点击 Home 按钮
        home_eating_button = self.browser.find_element_by_id("id_home_eating").click()

        # 发现 URL 又变回来了, 显示的还是 home 的菜单
        self.assertEqual(home_url, self.browser.current_url)

    def test_random_choice_eating_buttons(self):
        """
        测试链接到 random_choice 吃饭的按钮
        """
        # Y 发现首页上有一个 random_eating 按钮, 点击一下
        random_eating_button = self.browser.find_element_by_id("id_random_eating")
        random_eating_button.click()

        # Y 发现界面显示了一个大转盘
        spinner = self.browser.find_element_by_id("id_spinner")

        # 它看到大转盘的指针颜色现在是无, 而且还有个 "Spin me" 按钮
        pointer_span = self.browser.find_element_by_id("id_pointer_span")
        self.assertEqual("", pointer_span.get_attribute("style"))

        # 它点击了 Spin me 按钮, 发现指针颜色变化了
        spin_me = self.browser.find_element_by_id("id_spin_me")
        spin_me.click()
        self.assertNotEqual("", pointer_span.get_attribute("style"))

        # Y 知道要吃啥了, 于是想返回首页
        self.browser.find_element_by_id("id_home_page").click()


if __name__ == "__main__":
    pass
