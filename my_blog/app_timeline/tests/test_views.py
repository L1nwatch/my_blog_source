#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 负责测试 timeline 这个 app 的各个视图函数

2017.07.07 新增测试, 确保 html 目录树层级正确
2017.06.29 新增两个测试, 用于测试 timeline 显示旅行事件这个视图函数
"""
# 自己的模块
from common_module.tests.basic_test import BasicTest
import my_constant as const

# 标准库
from bs4 import BeautifulSoup

__author__ = '__L1n__w@tch'


class TestTravelEventTimeline(BasicTest):
    unique_url = const.TRAVEL_EVENT_TIMELINE_URL

    def test_travel_event_timeline_use_right_template(self):
        response = self.client.get(self.unique_url)

        self.assertTemplateUsed(response, const.TRAVEL_EVENT_TIMELINE_TEMPLATE)

    def test_travel_event_timeline_display_right_information(self):
        """
        测试会显示日期
        """
        response = self.client.get(self.unique_url)

        self.assertContains(response, "June")
        self.assertContains(response, "28")

    def test_travel_event_timeline_has_right_evt_format(self):
        """
        测试一个 div 内的格式是否正确
        """
        response = self.client.get(self.unique_url)

        html_parse = BeautifulSoup(response.content)  # 传入 html 源码
        events = html_parse.find_all("div", {"class": "evt"})  # 查找指定 tag, 指定要求有 class 属性
        self.assertTrue(len(events) > 0)

        for each_evt in events:  # 遍历所有查找结果
            # evt 下一个 div 应该是 in, 且只有一个
            in_div = each_evt.find_all("div", {"class": "in"})  # 在该节点中继续寻找指定 tag
            self.assertIsNotNone(in_div)
            self.assertTrue(len(in_div) == 1)

            # in_div 下一个 span 应该是 date, span 里面又有 2 个 span, 分别是: day/month
            span_tag = in_div[0].find_next("span")
            self.assertTrue("date" in span_tag.attrs["class"])
            child_span_tags = span_tag.find_all("span")
            self.assertTrue(any(
                ["day" in each_span.attrs["class"] for each_span in child_span_tags]  # 获取 class 属性
            ))
            self.assertTrue(any(
                ["month" in each_span.attrs["class"] for each_span in child_span_tags]
            ))

            # in_div 下一个 h2 为标题, 有且只有一个
            h2_tag = in_div[0].find_all("h2")
            self.assertTrue(len(h2_tag) == 1)

            # in_div 下有若干个 p, 作为 data 显示的 element
            data_tags = in_div[0].find_all("p", {"class": "data"})
            self.assertTrue(len(data_tags) >= 0)


if __name__ == "__main__":
    pass
