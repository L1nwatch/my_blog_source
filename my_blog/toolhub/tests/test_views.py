#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 对 toolhub 这个 APP 进行相关的视图测试

2017.10.14 补充 caesar 的测试
2017.06.14 新增有关返回静态 HTML 的视图函数测试
2017.03.25 新增有关 form 的测试
2017.03.24 编写有关视图首页的测试
"""
# 标准库
import os
from django.test import override_settings

# 自己的模块
from common_module.tests.basic_test import BasicTest
from common_module.common_help_function import is_static_file_exist
from toolhub.views import tools_name_list
from toolhub.forms import GitHubTranslateTextareaForm,CaesarCipherTextareaForm
import my_constant as const

__author__ = '__L1n__w@tch'


class HomeViewTest(BasicTest):
    unique_url = const.TOOLHUB_HOME_URL

    def test_use_right_template(self):
        """
        测试首页使用了正确的模板
        """
        response = self.client.get(self.unique_url)
        self.assertTemplateUsed(response, "toolhub_home.html")

    def test_display_all_tool_name(self):
        """
        首页应该显示所有工具的名字
        """
        response = self.client.get(self.unique_url)

        for each_tool_name in tools_name_list:
            self.assertContains(response, each_tool_name)


class GitHubPictureTranslateViewTest(BasicTest):
    unique_url = const.TOOLHUB_GITHUB_PICTURE_TRANSLATE_URL
    data_url = const.TOOLHUB_GITHUB_PICTURE_TRANSLATE_DATA_URL

    def test_use_right_template(self):
        response = self.client.get(self.unique_url)
        self.assertTemplateUsed(response, "github_picture_translate_tool/github_picture_translate_tool.html")

    def test_translate_right(self):
        response = self.client.post(self.data_url, {"raw_data": "2017-03-17首页截图.jpg"})
        right_answer = "2017-03-17%E9%A6%96%E9%A1%B5%E6%88%AA%E5%9B%BE.jpg"
        self.assertEqual(response.content.decode("utf8"), right_answer)

    def test_use_form(self):
        response = self.client.get(self.unique_url)
        self.assertIsInstance(response.context["textarea_form"], GitHubTranslateTextareaForm)


class CaesarCipherViewTest(BasicTest):
    unique_url = const.TOOLHUB_CAESAR_CIPHER_URL
    data_url = const.TOOLHUB_CAESAR_CIPHER_DATA_URL

    def test_use_right_template(self):
        response = self.client.get(self.unique_url)
        self.assertTemplateUsed(response, "caesar_cipher/caesar_cipher.html")

    def test_translate_right(self):
        response = self.client.post(self.data_url, {"raw_data": "zobD*ooC"})
        right_answer = "shU6*hh5"
        self.assertEqual(response.content.decode("utf8"), right_answer)

    def test_use_form(self):
        response = self.client.get(self.unique_url)
        self.assertIsInstance(response.context["textarea_form"], CaesarCipherTextareaForm)


@override_settings(DEBUG=False)  # 必须将 DEBUG 调成 False, 要不然会导致 debug_toolbar 出错
class StaticHTMLViewTest(BasicTest):
    """
    测试返回静态 HTML 的相关视图
    """
    static_htmls_path = const.STATIC_HTMLS_PATH
    unique_url = const.TOOLHUB_STATIC_HTML_URL

    def test_can_return_exist_html_file(self):
        """
        测试能够成功返回存在的 HTML 文件
        """
        # 确认文件存在
        test_file_name = "标准正态分布 Z 值表.html"
        self.assertTrue(is_static_file_exist(test_file_name))

        # 试图读取该 html
        response = self.client.get(self.unique_url.format(test_file_name))

        self.assertTemplateUsed(response, os.path.join("static_htmls", test_file_name))

    def test_return_404_while_html_not_exist(self):
        """
        测试当访问不存在的 html 文件时返回 404
        """
        # 确认文件不存在
        test_file_name = "{}.html".format(self.get_random_string(10))
        self.assertFalse(is_static_file_exist(test_file_name))

        # 试图读取该 html
        response = self.client.get(self.unique_url.format(test_file_name))
        # 返回了 404
        self.assertEqual(response.status_code, 404)

    def test_return_404_while_not_visit_html(self):
        """
        测试当访问非 html 文件时返回 404
        """
        # 不包含截断符的访问
        test_file_name = "{}".format(self.get_random_string(10))
        test_file_path = os.path.join(self.static_htmls_path, test_file_name)
        try:
            # 创建该文件, 以便测试使用
            with open(test_file_path, "w") as f:
                f.write("a")
            self.assertTrue(is_static_file_exist(test_file_name))

            # 试图读取该 html
            response = self.client.get(self.unique_url.format(test_file_name))
            # 返回了 404
            self.assertTrue(response.status_code, 404)
        finally:
            # 删除创建的测试文件
            if os.path.exists(test_file_path):
                os.remove(test_file_path)

