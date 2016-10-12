#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""

2016.10.07 添加了 ArticleForm 后要进行测试
"""

from articles.forms import ArticleForm
from django.test import TestCase
from my_constant import const

__author__ = '__L1n__w@tch'


# TODO: form 表单在搜索的时候老是 is_valid 验证失败
class ArticleFormTest(TestCase):
    def test_form_item_input_has_placeholder_and_css_classes(self):
        """
        测试表单是否包含了 PLACE_HOLDER/class/id 属性
        :return:
        """
        article_form = ArticleForm()
        self.assertIn('placeholder="{}"'.format(const.PLACE_HOLDER), article_form.as_p())
        self.assertIn('class="pure-input-2-3"', article_form.as_p(), "class 属性没有设置?还是说设置错了?")
        self.assertIn('id="id_search"', article_form.as_p(), "id 属性没有设置?还是说设置错了?")

    def test_form_validation_for_blank_input(self):
        form = ArticleForm(data={"title": ""})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["title"], [const.EMPTY_ARTICLE_ERROR])


if __name__ == "__main__":
    pass
