#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.01.31 发现对自定义 markdown 解析方法有要求, 所以还是写个单元测试吧
"""
from django.test import TestCase
from articles.templatetags.custom_filter import remove_code_tag_in_h_tags, add_em_tag

__author__ = '__L1n__w@tch'


class TestCustomMarkdown(TestCase):
    def test_remove_code_tag_in_h_tags(self):
        # 只有一个的情况
        test_data = "<h1>aaa<code>bbb</code></h1>"
        right_answer = "<h1>aaabbb</h1>"
        my_answer = remove_code_tag_in_h_tags(test_data)
        self.assertEqual(right_answer, my_answer)

        # 多个的情况
        test_data = "<h1>aaa<code>bbb</code></h1>\n<h2>aaa<code>bbb</code>ccc</h2>"
        right_answer = "<h1>aaabbb</h1>\n<h2>aaabbbccc</h2>"
        my_answer = remove_code_tag_in_h_tags(test_data)
        self.assertEqual(right_answer, my_answer)

        # 多个 code 的情况
        test_data = "<h1>aaa<code>bbb</code>ccc<code>ddd</code></h1>"
        right_answer = "<h1>aaabbbcccddd</h1>"
        my_answer = remove_code_tag_in_h_tags(test_data)
        self.assertEqual(right_answer, my_answer)


class TestCustomFilter(TestCase):
    def test_add_em_tag(self):
        """
        给前端用的, 对每个关键词添加 em 标签, 方便前端显示
        """
        test_data = "aaa-user = aaa"
        right_answer = "user = <em>aaa</em>"
        my_answer = add_em_tag(test_data)
        self.assertEqual(right_answer, my_answer)

        test_data = "aaa-user = aAa"
        right_answer = "user = <em>aAa</em>"
        my_answer = add_em_tag(test_data)
        self.assertEqual(right_answer, my_answer)


if __name__ == "__main__":
    pass
