#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 测试 homepage 这个 app 下的视图函数

2021-10-10 first unittest
"""
# 自己的模块
from common_module.tests.basic_test import BasicTest
import my_constant as const

__author__ = '__L1n__w@tch'


class TestHomePage(BasicTest):
    unique_url = const.HOMEPAGE_URL

    def test_homepage_use_right_template(self):
        response = self.client.get(self.unique_url)
        self.assertTemplateUsed(response, const.HOMEPAGE_TEMPLATE)
