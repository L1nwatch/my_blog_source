#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.03.26 新增有关搜索输入的测试代码
2017.03.23 新增有关搜索结果排序的测试
2017.03.07 为共有函数进行测试编写
"""
import string
import random

from django.test import TestCase
from my_constant import const
from articles.common_help_function import clean_form_data, sort_search_result, data_check
from articles.models import Article

__author__ = '__L1n__w@tch'


class TestCommonHelpFunc(TestCase):
    def test_clean_form_data(self):
        # 测试 "aa ", 应该得到 "aa"
        test_data = "aa "
        right_answer = "aa"
        my_answer = clean_form_data(test_data)
        self.assertEqual(right_answer, my_answer)

        # 测试 "aa bb", 应该得到 "aa bb"
        test_data = "aa bb"
        right_answer = "aa bb"
        my_answer = clean_form_data(test_data)
        self.assertEqual(right_answer, my_answer)

        # 测试 " bb", 应该得到 "bb"
        test_data = " bb"
        right_answer = "bb"
        my_answer = clean_form_data(test_data)
        self.assertEqual(right_answer, my_answer)

        # 测试 "test_article", 应该得到 "test_article"
        test_data = "test_article "
        right_answer = "test_article"
        my_answer = clean_form_data(test_data)
        self.assertEqual(right_answer, my_answer)

    def test_sort_search_result(self):
        test_article1 = Article.objects.create(title="test 3rd", content="test")
        test_article2 = Article.objects.create(title="test 1st", content="test test tEsT")
        test_article3 = Article.objects.create(title="test 2nd", content="tESt test")

        test_result_list = [
            const.ARTICLE_STRUCTURE(test_article1.id, test_article1.title, "aaa", "articles"),
            const.ARTICLE_STRUCTURE(test_article2.id, test_article2.title, "bbb", "articles"),
            const.ARTICLE_STRUCTURE(test_article3.id, test_article3.title, "ccc", "articles"),
        ]
        right_answer = [
            const.ARTICLE_STRUCTURE(test_article2.id, test_article2.title, "bbb", "articles"),
            const.ARTICLE_STRUCTURE(test_article3.id, test_article3.title, "ccc", "articles"),
            const.ARTICLE_STRUCTURE(test_article1.id, test_article1.title, "aaa", "articles"),
        ]
        my_answer = sort_search_result(test_result_list, {"test"})
        self.assertEqual(len(my_answer), 3)
        for each_right, each_mine in zip(right_answer, my_answer):
            self.assertEqual(each_right, each_mine)

    def test_data_check(self):
        # 单个字符(仅限英文、数字、特殊字符)的输入, 都认为非法
        # 单个中文
        test_data = "啊"
        self.assertTrue(data_check(test_data))

        # 单个非中文
        for each_char in string.printable:
            self.assertFalse(data_check(each_char))

        # 多个字符, 如果全是特殊字符, 则认为非法
        # 含非特殊字符
        for i in range(100):
            test_data = random.choice(string.ascii_letters + string.digits) + "".join(
                [random.choice(string.punctuation) for j in range(random.randint(2, 30))])
            self.assertTrue(data_check(test_data))

        # 不含非特殊字符
        for i in range(100):
            test_data = "".join([random.choice(string.punctuation) for j in range(random.randint(2, 100))])
            self.assertFalse(data_check(test_data))


if __name__ == "__main__":
    pass
