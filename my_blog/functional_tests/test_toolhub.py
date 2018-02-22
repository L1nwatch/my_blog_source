#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 给 toolhub 的各个工具编写相关测试代码

2017.12.03 解决 chrome 自动化测试的 BUG
2017.10.14 新增凯撒密码的相关测试
2017.06.23 新增一个跳转到实验规模计算的选项卡
2017.06.22 补充 ToolHub 选项卡的测试
2017.06.15 增加有关访问 html 文件的相关功能测试
2017.06.14 新增有关 AB 测试中打开正态函数分数表的功能测试
2017.04.04 新增超链接到凯撒密码工具的相关测试
2017.03.24 开始编写 toolhub, 先给 GitHub 图片地址转换器编写相关测试代码
"""
# 标准库
import os
import unittest
import requests
import html

# 自己的模块
from functional_tests.base import FunctionalTest
from common_module.common_help_function import is_static_file_exist
import my_constant as const

__author__ = '__L1n__w@tch'


class TestEncoding(FunctionalTest):
    unique_url = const.TOOLHUB_HOME_URL

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
    unique_url = const.TOOLHUB_HOME_URL

    def setUp(self):
        self.toolhub_home = "{host}{path}".format(host=self.server_url, path=self.unique_url)
        super().setUp()

    @unittest.skipUnless(const.SLOW_CONNECT_DEBUG, "[*] 用户选择忽略部分测试")
    def test_caesar_cipher(self):
        """
        测试凯撒密码的超链接正常
        """
        # Y 打开 toolhub 首页,
        self.browser.get(self.toolhub_home)
        home_url = self.browser.current_url

        # 点击一下, 发现链接跳转了

        # 界面上出现了凯撒密码对应的加密解密操作
        self.assertIn("Caesar Cipher", self.browser.page_source)

        # Y 很满意, 于是点击首页看看其他内容
        self.browser.back()
        home_view = self.browser.find_element_by_id("id_home_page")
        home_view.click()

    def test_caesar_cipher_decrypt_right(self):
        """
        测试转换功能正常使用
        """
        # Y 打开了 toolhub 的首页, 发现凯撒密码
        self.browser.get(self.toolhub_home)
        home_url = self.browser.current_url

        # 它点击了一下这个工具的链接, 发现页面上出现了一个输入框, 还有一个转换按钮
        self.browser.execute_script('document.getElementById("id_caesar_cipher").click()')
        self.assertNotEqual(home_url, self.browser.current_url)

        input_box = self.browser.find_element_by_id("id_input_box")
        translate_button = self.browser.find_element_by_id("id_caesar_decrypt_button")

        # Y 在输入框里面输入了一堆内容, 再点击了一下转换按钮
        input_box.send_keys("zobD*ooC")
        translate_button.click()

        # 它发现输出框显示出了转换之后的结果
        output_box = self.browser.find_element_by_id("id_output_box")
        right_answer = "shU6*hh5"
        self.assertEqual(output_box.get_attribute("value"), right_answer)

        # Y 很满意, 点击首页想看看其他内容
        home_view = self.browser.find_element_by_id("id_home_page")
        home_view.click()

    def test_caesar_cipher_encrypt_right(self):
        """
        测试转换功能正常使用
        """
        # Y 打开了 toolhub 的首页, 发现凯撒密码
        self.browser.get(self.toolhub_home)
        home_url = self.browser.current_url

        # 它点击了一下这个工具的链接, 发现页面上出现了一个输入框, 还有一个转换按钮
        self.browser.execute_script('document.getElementById("id_caesar_cipher").click()')
        self.assertNotEqual(home_url, self.browser.current_url)

        input_box = self.browser.find_element_by_id("id_input_box")
        translate_button = self.browser.find_element_by_id("id_caesar_encrypt_button")

        # Y 在输入框里面输入了一堆内容, 再点击了一下转换按钮
        input_box.send_keys("shU6*hh5")
        translate_button.click()

        # 它发现输出框显示出了转换之后的结果
        output_box = self.browser.find_element_by_id("id_output_box")
        right_answer = "zobD*ooC"
        self.assertEqual(output_box.get_attribute("value"), right_answer)

        # Y 很满意, 点击首页想看看其他内容
        home_view = self.browser.find_element_by_id("id_home_page")
        home_view.click()


class TestABTesting(FunctionalTest):
    """
    测试有关 AB 测试选项卡的相关功能
    """
    unique_url = const.TOOLHUB_HOME_URL

    def setUp(self):
        self.toolhub_home = "{host}{path}".format(host=self.server_url, path=self.unique_url)
        super().setUp()

    def test_options_exist(self):
        """
        测试 toolhub 的各个选项卡存在
        """
        # Y 打开了 ToolHub 首页, 想看看描述中的每一个选项卡是不是都在这个页面中
        self.browser.get(self.toolhub_home)

        # 它先查看了所有一级选项卡
        for each_option in const.TOOLHUB_LEVEL_ONE_OPTIONS:
            self.assertIn(html.escape(each_option), self.browser.page_source,
                          "\n[-] 不存在 {} 这个选项卡\n".format(each_option))

        # 然后查看了所有二级选项卡
        for each_option in const.TOOLHUB_LEVEL_TWO_OPTIONS:
            self.assertIn(each_option, self.browser.page_source, "\n[-] 不存在 {} 这个选项卡\n".format(each_option))

        # 最后又查看了所有三级选项卡
        for each_option in const.TOOLHUB_LEVEL_THREE_OPTIONS:
            self.assertIn(each_option, self.browser.page_source, "\n[-] 不存在 {} 这个选项卡\n".format(each_option))

    def test_ab_testing_has_z_value_table_link(self):
        """
        测试 AB 测试界面含有 z 值表的链接
        """
        # Y 打开了 ToolHub 首页, 它知道有 "正态函数分布 Z 值表" 这么一个选项卡, 于是想访问看看
        self.browser.get(self.toolhub_home)
        home_url = self.browser.current_url

        self.browser.execute_script('document.getElementById("id_ab_testing_z_value_table").click()')

        # 发现点击完之后页面跳转了, 出现了个大标题是正态函数分布 Z 值表, 然后还有各种表格
        self.assertNotEqual(home_url, self.browser.current_url)  # 点击完之后 URL 变化了
        self.assertIn("标准正态分布 Z 值表", self.browser.page_source)
        self.assertIn("<table>", self.browser.page_source)

    def test_ab_testing_sample_size_calculator_link(self):
        """
        测试能够通过选项卡跳转到实验规模计算工具上
        """
        # Y 打开了 ToolHub 首页, 它知道这个页面上有个选项卡叫做 xxxx, 于是直接去访问这个选项卡
        self.browser.get(self.toolhub_home)
        self.browser.execute_script('document.getElementById("ib_ab_testing_sample_size").click()')

        # 发现 URL 变化了, 网页跳转到了这个在线计算工具的页面上
        self.assertEqual(self.browser.current_url, const.TOOLHUB_AB_TESTING_SAMPLE_SIZE_URL)


class TestStaticHTML(FunctionalTest):
    """
    测试有关读取静态 HTML 页面
    """
    unique_url = const.TOOLHUB_STATIC_HTML_URL

    def setUp(self):
        self.static_file_uri = "{host}{path}".format(host=self.server_url, path=self.unique_url)
        super().setUp()

    def test_return_404_while_html_not_exist(self):
        """
        测试当访问不存在的 html 文件时返回 404
        """
        # Y 知道某个页面不存在于服务器之中
        test_file_name = "{}.html".format(self.get_random_string(10))
        self.assertFalse(is_static_file_exist(test_file_name))

        # 但是 Y 还是想访问看看, 看下访问不存在的 html 时会出现什么情况
        self.browser.get(self.static_file_uri.format(test_file_name))
        response = requests.get(self.static_file_uri.format(test_file_name))

        # 返回了 404
        self.assertEqual(response.status_code, 404)

    def test_return_404_while_not_visit_html(self):
        """
        测试访问非 html 文件时返回 404
        :return:
        """
        # Y 知道某个文件存在, 但它不是 html 文件, 想试试看能不能通过这个接口访问该文件
        test_file_name = "{}".format(self.get_random_string(10))
        test_file_path = os.path.join(const.STATIC_HTMLS_PATH, test_file_name)
        try:
            # Y 确保想要访问的文件是存在的
            with open(test_file_path, "w") as f:
                f.write("a")
            self.assertTrue(is_static_file_exist(test_file_name))

            # 接着 Y 开始试图访问这个文件了
            self.browser.get(self.static_file_uri.format(test_file_name))
            response = requests.get(self.static_file_uri.format(test_file_name))

            # 返回了 404
            self.assertEqual(response.status_code, 404)
        finally:
            # Y 好心的删除了测试文件, 防止被管理员发现
            if os.path.exists(test_file_path):
                os.remove(test_file_path)

    def test_visit_html_file_using_cut_char(self):
        """
        测试通过截断符访问 html 是否能成功
        """

        # Y 最近刚学了点 Web 渗透, 想试试通过包含截断符看能否成功访问
        test_string = self.get_random_string(10)
        test_file_name = "{}%00.html".format(test_string)
        right_file_name = "{}.html".format(test_string)
        right_file_path = os.path.join(const.STATIC_HTMLS_PATH, right_file_name)
        try:
            # Y 创建了这个文件, 即 xxx.html
            with open(right_file_path, "w") as f:
                f.write("a")
            self.assertTrue(is_static_file_exist(right_file_name))

            # 然后 Y 通过截断符访问了 xxx%00.html, 看会咋样
            with self.assertRaises(Exception):
                self.browser.get(self.static_file_uri.format(test_file_name))

            # 用 requests 库访问结果也是一样的
            response = requests.get(self.static_file_uri.format(test_file_name))

            # Y 发现网页返回了 500, 服务器错误
            self.assertEqual(response.status_code, 500)
        finally:
            # 删除创建的测试文件
            if os.path.exists(right_file_path):
                os.remove(right_file_path)
