#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 负责测试错误页面, 比如 404 页面等

2017.06.21 新增 404 页面的测试
"""
# 标准库
from django.test import override_settings
import requests

# 自己的模块
from .base import FunctionalTest

__author__ = '__L1n__w@tch'


@override_settings(DEBUG=False)
class Test404Pages(FunctionalTest):
    """
    负责测试 404 页面相关的代码逻辑
    """

    def setUp(self):
        self.not_exist_url = "{}/aaa".format(self.server_url)
        super().setUp()

    def test_show_404_pages_when_visit_not_exist_url(self):
        """
        测试访问不存在的 URL 时会显示 404 页面
        """

        # Y 知道某个 url 不存在, 于是 Y 访问了该 URL
        response = requests.get(self.not_exist_url)
        # Y 发现服务返回了 404 码
        self.assertTrue(response.status_code == 404)
        # 而且该 404 页面用的是自定义的模板页面
        self.browser.get(self.not_exist_url)
        self.assertTrue("The page you requested cannot be found right meow." in self.browser.page_source)

        # Y 在想是不是所有页面访问都会得到 404, 于是它试着访问了一下首页
        response = requests.get(self.server_url)
        # 发现首页能够正常访问, 并不是返回 404 码, 首页存在标志性的搜索框
        self.assertFalse(response.status_code == 404)
        self.browser.get(self.server_url)
        search_input = self.browser.find_element_by_id("id_search")
        self.assertIsNotNone(search_input)

