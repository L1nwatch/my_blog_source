#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2016.10.04 针对布局和样式的功能测试, 这里只是简单的检查一下是不是两种浏览器窗口下首页按钮是否按照原来的方式显示
"""
from .base import FunctionalTest

__author__ = '__L1n__w@tch'


class LayoutStylingTest(FunctionalTest):
    def test_home_page_button_at_right_position(self):
        """
        不管后期如何调动, 首页按钮肯定要么是在左边中间的第一个位置, 要么是在上面中间的第一个位置
        :return:
        """
        # Y 访问首页
        self.browser.get(self.server_url)

        # 看到首页按钮被放置在左边中间的第一个位置
        home_page_button = self.browser.find_element_by_id("id_home_page")
        self.assertAlmostEqual(home_page_button.location["x"], 87, delta=5)
        self.assertAlmostEqual(home_page_button.location["y"], 321, delta=5)

        # Y 调整了一下窗口大小
        self.browser.set_window_size(640, 800)

        # 看到首页按钮变成了上面中间的第一个位置
        home_page_button = self.browser.find_element_by_id("id_home_page")
        self.assertAlmostEqual(home_page_button.location["x"], 151, delta=5)
        self.assertAlmostEqual(home_page_button.location["y"], 111, delta=5)


if __name__ == "__main__":
    pass
