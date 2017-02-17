#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.02.08 重定义一个基类, 作为 Journal 和 Article 的 Form
2016.10.07 添加了 ArticleForm 后要进行测试
"""

from articles.forms import ArticleForm, BaseSearchForm
from django.test import TestCase
from my_constant import const

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

    def test_form_validation_for_blank_input(self):
        form = BaseSearchForm(data={"title": ""})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["title"], [const.EMPTY_ARTICLE_ERROR])


class ArticleFormTest(TestCase):
    def test_form_item_input_has_placeholder_and_css_classes(self):
        """
        测试 Article 表单是否包含了 class 属性
        :return:
        """
        article_form = ArticleForm()
        self.assertIn('class="pure-input-2-3"', article_form.as_p(), "class 属性没有设置?还是说设置错了?")


if __name__ == "__main__":
    pass
