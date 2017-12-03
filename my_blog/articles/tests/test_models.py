#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.05.21 添加字段 click_times, 用来表示访问次数的, 因此也添加相关 model 测试
2017.04.03 重构一下创建测试数据的代码, 将其分离出来单独作为一个基类了
2017.03.15 要提供搜索选项的功能, 需要重构一下搜索的 Form, 甚至连对应的 Model 都要修改, 于是编写测试
2016.10.28 将原来的时间改为创建时间, 另外新增一个更新时间的字段, 所以需要进行 model 测试
"""

from common_module.tests.basic_test import BasicTest
import my_constant as const

__author__ = '__L1n__w@tch'


class SearchModelTest(BasicTest):
    def test_has_search_content_and_choice_fields(self):
        """
        测试该 model 含有搜索内容和搜索选项这两个字段
        """
        search_content = "这是我要搜索的内容"
        choice = "all"

        new_search = self.create_search(search_content=search_content, search_choice=choice)
        self.assertEqual(new_search.search_content, search_content)
        self.assertEqual(new_search.search_choice, choice)

    def test_choice_field_has_limit_value(self):
        """
        测试该 model 的 search_choice 字段只能是指定值: ["All", "GitBooks", "Articles", "Code", "Journals"]
        """
        choices = ["all", "gitbooks", "articles", "code", "journals"]
        # 正确输入, 不会报错
        for each_right_choice in choices:
            self.create_search(search_choice=each_right_choice)

        # 错误输入, 会报错
        wrong_choice = "not_exist_choice"
        with self.assertRaises(RuntimeError):
            self.create_search(search_choice=wrong_choice)

    def test_choice_field_ignore_case(self):
        """
        测试 model 会自动把所有字段都转换为小写
        """
        # 测试 search_content 字段的大小写转换
        search_content = "I HaVe bIg letters"
        choice = "aLL"

        new_search = self.create_search(search_content=search_content, search_choice=choice)
        self.assertEqual(new_search.search_content, search_content.lower())
        self.assertEqual(new_search.search_choice, choice.lower())

    def test_help_text_default_value(self):
        """
        测试各个字段有其固定的帮助信息
        """
        new_search = self.create_search()
        self.assertEqual(new_search._meta.get_field("search_content").help_text, const.SEARCH_CONTENT_HELP_TEXT)
        self.assertEqual(new_search._meta.get_field("search_choice").help_text, const.SEARCH_CHOICE_HELP_TEXT)


class ArticleModelTest(BasicTest):
    def test_has_create_time_and_update_time(self):
        new_article = self.create_article()

        self.assertNotEqual(new_article.create_time, None)
        self.assertNotEqual(new_article.update_time, None)

    def test_create_time_equal_to_update_time_when_create_new_article(self):
        """
        新建一篇文章时, 文章的创建时间和更新时间应该是一样的
        :return:
        """
        new_article = self.create_article()

        create_time = "{}/{}/{}/{}".format(new_article.create_time.year, new_article.create_time.month,
                                           new_article.create_time.day, new_article.create_time.hour)
        update_time = "{}/{}/{}/{}".format(new_article.update_time.year, new_article.update_time.month,
                                           new_article.update_time.day, new_article.update_time.hour)
        self.assertEqual(create_time, update_time)

    def test_has_default_visited_times(self):
        """
        测试创建文章之后初始的访问次数应该为 0
        """
        new_article = self.create_article()
        self.assertEqual(new_article.click_times, 0)
