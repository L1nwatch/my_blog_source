#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 负责测试 timeline 这个 app 的各个视图函数

2017.06.29 新增两个测试, 用于测试 timeline 显示旅行事件这个视图函数
"""
# 自己的模块
from common_module.tests.basic_test import BasicTest
import my_constant as const

__author__ = '__L1n__w@tch'


class TestTravelEventTimeline(BasicTest):
    unique_url = const.TRAVEL_EVENT_TIMELINE_URL

    def test_travel_event_timeline_use_right_template(self):
        response = self.client.get(self.unique_url)

        self.assertTemplateUsed(response, const.TRAVEL_EVENT_TIMELINE_TEMPLATE)

    def test_travel_event_timeline_display_right_information(self):
        response = self.client.get(self.unique_url)

        self.assertContains(response, "June")
        self.assertContains(response, "28")


if __name__ == "__main__":
    pass
