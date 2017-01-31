#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.01.31 发现对自定义 markdown 解析方法有要求, 所以还是写个单元测试吧
"""
from django.test import TestCase
from articles.templatetags.custom_markdown import remove_code_tag_in_h_tags

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


if __name__ == "__main__":
    pass
