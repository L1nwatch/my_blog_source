#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.06.14 给 Input 标签添加 class 属性
2017.03.17 设置所有页面都不显示 select_choice, 于是新编 form 测试
2017.03.15 要提供搜索选项的功能, 需要重构一下搜索的 Form, 于是修改测试
2017.02.08 重定义一个基类, 作为 Journal 和 Article 的 Form
2016.10.07 添加了 ArticleForm 后要进行测试
"""

from articles.forms import ArticleForm, BaseSearchForm
from django.test import TestCase
import my_constant as const

__author__ = '__L1n__w@tch'


class BaseSearchFormTest(TestCase):
    def test_form_item_input_has_placeholder_and_css_classes(self):
        """
        测试 Base 表单是否包含了 PLACE_HOLDER/id 属性
        :return:
        """
        base_search_form = BaseSearchForm()
        self.assertIn('placeholder="{}"'.format(const.PLACE_HOLDER), base_search_form.as_p())
        self.assertIn('id="id_search"', base_search_form.as_p(), "id 属性没有设置?还是说设置错了?")
        self.assertIn('class="pure-input-2-3"', base_search_form.as_p(), "class 属性没有设置?还是说设置错了?")

    def test_form_validation_for_blank_input(self):
        form = BaseSearchForm(data={"search_content": ""})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["search_content"], [const.EMPTY_ARTICLE_ERROR])

    def test_not_show_select_choice(self):
        """
        要求所有页面都不显示 search_choice, 只要测试基类 basesearch 即可
        """
        base_search_form = BaseSearchForm()
        self.assertIn('style="display:none"', base_search_form.as_p())


class ArticleFormTest(TestCase):
    def test_form_item_input_has_placeholder_and_css_classes(self):
        """
        测试 Article 表单是否包含了 class 属性
        :return:
        """
        article_form = ArticleForm()
        self.assertIn('class="pure-input-2-3"', article_form.as_p(), "class 属性没有设置?还是说设置错了?")

