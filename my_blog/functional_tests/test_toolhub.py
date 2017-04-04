#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 给 toolhub 的各个工具编写相关测试代码

2017.04.04 新增超链接到凯撒密码工具的相关测试
2017.03.24 开始编写 toolhub, 先给 GitHub 图片地址转换器编写相关测试代码
"""
import unittest

from functional_tests.base import FunctionalTest
from my_constant import const

__author__ = '__L1n__w@tch'


class TestEncoding(FunctionalTest):
    unique_url = "/tool_hub/"

    def setUp(self):
        self.toolhub_home = "{host}{path}".format(host=self.server_url, path=self.unique_url)
        super().setUp()

    def test_translate_right(self):
        """
        测试转换功能正常使用
        """
        # Y 打开了 toolhub 的首页, 发现了 GitHub 图片地址转换
        self.browser.get(self.toolhub_home)
        home_url = self.browser.current_url

        # 它点击了一下这个工具的链接, 发现页面上出现了一个输入框, 还有一个转换按钮
        self.browser.execute_script('document.getElementById("id_github_picture_translate").click()')
        self.assertNotEqual(home_url, self.browser.current_url)

        input_box = self.browser.find_element_by_id("id_input_box")
        translate_button = self.browser.find_element_by_id("id_translate_button")

        # Y 在输入框里面输入了一堆内容, 再点击了一下转换按钮
        input_box.send_keys("2017-03-17首页截图.jpg")
        translate_button.click()

        # 它发现输出框显示出了转换之后的结果
        output_box = self.browser.find_element_by_id("id_output_box")
        right_answer = "2017-03-17%E9%A6%96%E9%A1%B5%E6%88%AA%E5%9B%BE.jpg"
        self.assertEqual(output_box.get_attribute("value"), right_answer)

        # Y 很满意, 点击首页想看看其他内容
        home_view = self.browser.find_element_by_id("id_home_page")
        home_view.click()


class TestCipher(FunctionalTest):
    unique_url = "/tool_hub/"

    def setUp(self):
        self.toolhub_home = "{host}{path}".format(host=self.server_url, path=self.unique_url)
        super().setUp()

    @unittest.skipUnless(const.SLOW_CONNECT_DEBUG, "[*] 用户选择忽略部分测试")
    def test_caesar_cipher(self):
        """
        测试凯撒密码的超链接正常
        """
        # Y 打开 toolhub 首页, 发现凯撒密码
        self.browser.get(self.toolhub_home)
        home_url = self.browser.current_url

        # 点击一下, 发现链接跳转了
        self.browser.execute_script('document.getElementById("id_caesar_cipher").click()')
        self.assertNotEqual(home_url, self.browser.current_url)
        self.assertEqual(self.browser.current_url,
                         "http://www.cryptool-online.org/index.php?option=com_cto&view=tool&Itemid=96&lang=en")

        # 界面上出现了凯撒密码对应的加密解密操作
        self.assertIn("Caesar Cipher", self.browser.page_source)

        # Y 很满意, 于是点击首页看看其他内容
        self.browser.back()
        home_view = self.browser.find_element_by_id("id_home_page")
        home_view.click()


if __name__ == "__main__":
    pass
