#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.01.27 处理一下表格解析错误的问题
2017.01.27 处理一下 ``` 后带空格会影响格式的问题, 最后发现是原来的 markdown 文件不标准导致的, 算了, 就当添加一个 markdown 显示测试吧
2016.10.28 添加关于两个时间的测试, 包括文章的创建时间以及文章的更新时间
2016.10.04 针对布局和样式的功能测试, 这里只是简单的检查一下是不是两种浏览器窗口下首页按钮是否按照原来的方式显示
"""
from .base import FunctionalTest
from articles.models import Article

import datetime
import unittest

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


class ArticleDisplayTest(FunctionalTest):
    def setUp(self):
        super().setUp()
        self._create_markdown_test_article()

    @staticmethod
    def _create_markdown_test_article():
        """
        创建一篇测试用的 markdown 文章
        :return:
        """
        # 1. 测试点: ``` 行中带空格

        with open("functional_tests/markdown_file_for_test.md", "r") as f:
            content1 = f.read()

        # 创建一篇 Markdown 文章, 含有测试用的各个内容
        Article.objects.create(title="code segment with white space", content=content1)

    def test_white_space_display_correct(self):
        """
        测试文章里面 ``` 后面跟着的东西带有空格, 是否显示正常
        比如某篇文章:
            ```sql lite
            watch
            ```
        会不会被 sql lite 中间的这个空格影响到接下来的排版?
        最后发现是这种写法本身就不标准(以 GitHub 为标准), 所以就不理了
        """
        # Y 访问首页
        self.browser.get(self.server_url)

        # Y 记得某篇文章使用了 ```sql lite, 想看看是否能显示正确, 于是找到待测试的那篇文章
        articles_after_search = self.browser.find_element_by_id("id_article_title")
        articles_after_search.click()

        # sql lite 不应该出现在文章中
        self.assertNotIn("sql lite", self.browser.find_element_by_tag_name('body').text)

    def test_tables_parse_correct(self):
        """
        测试解析器能否正确解析 table 文章
        :return:
        """
        # Y 访问首页
        self.browser.get(self.server_url)

        # Y 记得某篇文章使用了表格, 想看看是否能显示正确, 于是找到待测试的那篇文章
        articles_after_search = self.browser.find_element_by_id("id_article_title")
        articles_after_search.click()

        # Y 检查 --- 是否出现在文章正文中, 出现了就说明没解析成功
        self.assertNotIn("---", self.browser.find_element_by_tag_name('body').text)

        # Y 记得还有些特殊符号在表格中, 想看下这些特殊符号是否能够显示出来
        self.assertIn("{:.2f}", self.browser.find_element_by_tag_name('body').text)

    def test_sidebar_button_display(self):
        """
        测试打开一篇文章的时候左边的菜单显示
        """
        # Y 访问首页
        self.browser.get(self.server_url)

        # Y 随便打开了一篇文章
        articles_after_search = self.browser.find_element_by_id("id_article_title")
        articles_after_search.click()

        # 发现左边的按钮变化了, 只剩下一个可以链接到首页的作者名以及一个搜索框
        sidebar = self.browser.find_element_by_id("id_sidebar")
        self.assertIn("w@tch", sidebar.text)
        self.assertNotIn("EMAIL", sidebar.text)
        search_button = self.browser.find_element_by_id("id_search")

        # TODO: Y 还发现左边显示了一堆目录树, 居然是跟右边的文章有一一对应关系的


        # TODO: Y 发现直接点击目录树, 右边就会跳转到对应的地方进行显示
        pass


if __name__ == "__main__":
    pass
