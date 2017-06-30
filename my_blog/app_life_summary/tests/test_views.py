#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 负责测试 life_summary 这个 APP 下的视图函数

2017.06.30 新增有关 life_summary 首页的视图测试
"""
# 标准库
from common_module.tests.basic_test import BasicTest

# 自己的模块
import my_constant as const

__author__ = '__L1n__w@tch'


class TestLifeSummary(BasicTest):
    unique_url = const.LIFE_SUMMARY_URL

    def test_life_summary_use_right_template(self):
        response = self.client.get(self.unique_url)
        self.assertTemplateUsed(response, const.LIFE_SUMMARY_TEMPLATE)

    def test_life_summary_display_right_information(self):
        response = self.client.get(self.unique_url)
        self.assertContains(response, "洗漱用品")
        self.assertContains(response, "生活习惯")


if __name__ == "__main__":
    pass
