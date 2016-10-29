#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2016.10.28 添加关于两个时间的测试, 包括文章的创建时间以及文章的更新时间
2016.10.04 针对布局和样式的功能测试, 这里只是简单的检查一下是不是两种浏览器窗口下首页按钮是否按照原来的方式显示
"""
from .base import FunctionalTest
import datetime

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
        self.assertAlmostEqual(home_page_button.location["x"], 133, delta=5)
        self.assertAlmostEqual(home_page_button.location["y"], 111, delta=5)


class ArticleTimeInfoTest(FunctionalTest):
    def setUp(self):
        super().setUp()
        self._create_test_db_data()
        self.test_time = datetime.datetime.now()

    def test_has_article_create_time(self):
        # 访问首页
        self.browser.get(self.server_url)

        # 发现存在创建时间的字样, 而且能看到格式是: "Y 年 m 月 d 号 H 时"
        self.browser.find_element_by_id("id_create_time")
        create_time_label_content = ("Create: {} 年 {} 月 {} 号 {} 时"
                                     .format(self.test_time.year, str(self.test_time.month).zfill(2),
                                             str(self.test_time.day).zfill(2), str(self.test_time.hour).zfill(2)))
        self.assertIn(create_time_label_content, self.browser.page_source)

    def test_has_article_update_time(self):
        # 访问首页
        self.browser.get(self.server_url)

        # 发现存在更新时间的字样, 而且能看到格式是: "Y 年 m 月 d 号 H 时"
        self.browser.find_element_by_id("id_update_time")
        update_time_label_content = ("Update: {} 年 {} 月 {} 号 {} 时"
                                     .format(self.test_time.year, str(self.test_time.month).zfill(2),
                                             str(self.test_time.day).zfill(2), str(self.test_time.hour).zfill(2)))
        self.assertIn(update_time_label_content, self.browser.page_source)

    def test_tag_html_has_right_time(self):
        """
        测试 tag.html 显示的时间是正确的
        :return:
        """
        # 访问首页
        self.browser.get(self.server_url)

        # 发现分类包含个超链接, 点击进去看看
        self.browser.find_element_by_id("id_category").click()

        # 出现了一个新页面, 页面上显示了每篇文章的发布时间
        publish_time_label_content = ("发布：{} 年 {} 月 {} 号 {} 时"
                                      .format(self.test_time.year, str(self.test_time.month).zfill(2),
                                              str(self.test_time.day).zfill(2), str(self.test_time.hour).zfill(2)))
        self.assertIn(publish_time_label_content, self.browser.page_source)


if __name__ == "__main__":
    pass
