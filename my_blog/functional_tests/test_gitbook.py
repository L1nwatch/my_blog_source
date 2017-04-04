#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.04.04 修正某个老是导致测试失败的 BUG(案例无问题)
2017.03.10 删除 GitBook 测试, 老是失败搞得我都没耐心了(网速问题)
2017.03.05 要开始写 GitBook 这个 APP 相关实现了, 于是先编测试文件
"""
from .base import FunctionalTest, DEFAULT_WAIT
from gitbook_notes.models import GitBook
from my_constant import const

import unittest

__author__ = '__L1n__w@tch'


class GitBookSearchTest(FunctionalTest):
    def setUp(self):
        self.create_gitbook_test_db_data()
        super().setUp()

    @unittest.skipUnless(const.SLOW_CONNECT_DEBUG, "[*] 用户选择忽略部分测试")
    def test_all_search_can_search_exist_gitbook(self):
        """
        测试进行 All 搜索时能搜索到 GitBook
        """
        test_gitbook = GitBook.objects.get(title="stackoverflow-about-Python/super与init方法")

        # Y 打开首页
        self.browser.get(self.server_url)

        # Y 知道某本 GitBook 里面含有关键词 "避免直接使用父类的名字", 于是搜索它
        search_button = self.browser.find_element_by_id("id_search")
        search_button.send_keys("{}\n".format("避免直接使用父类的名字"))

        # Y 看到搜索结果中确实显示了某个 GitBook 以及对应行的内容
        self.assertIn(test_gitbook.title, self.browser.page_source)
        self.assertIn("避免直接使用父类的名字", self.browser.page_source)
        self.assertNotIn(const.EMPTY_ARTICLE_ERROR, self.browser.page_source)

    def test_all_search_can_not_search_not_exist_gitbook(self):
        """
        测试进行 All 搜索时, 如果不存在对应的关键词会显示搜索结果为空
        """
        # Y 打开首页
        self.browser.get(self.server_url)

        # 它知道不管是 GitBook 还是 Articles 还是 journals 都没有含关键词 "not_exist_key_word" 的文章
        # 于是它故意搜索这个关键词, 看能显示出什么
        search_button = self.browser.find_element_by_id("id_search")
        search_button.send_keys("{}\n".format("not_exist_key_word"))

        # 结果发现搜索页面提示搜索结果为空
        self.assertIn(const.EMPTY_ARTICLE_ERROR, self.browser.page_source)


if __name__ == "__main__":
    pass
