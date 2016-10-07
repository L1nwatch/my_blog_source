#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""

2016.10.07 添加了 ArticleForm 后要进行测试
"""

from django.test import TestCase

from articles.forms import ArticleForm, EMPTY_ARTICLE_ERROR, PLACE_HOLDER

__author__ = '__L1n__w@tch'


class ArticleFormTest(TestCase):
    def test_form_item_input_has_placeholder_and_css_classes(self):
        """
        测试表单是否包含了 PLACE_HOLDER/class/id 属性
        :return:
        """
        article_form = ArticleForm()
        self.assertIn('placeholder="{}"'.format(PLACE_HOLDER), article_form.as_p())
        self.assertIn('class="pure-input-3-3"', article_form.as_p(), "class 属性没有设置?还是说设置错了?")
        self.assertIn('id="id_search"', article_form.as_p(), "id 属性没有设置?还是说设置错了?")

    def test_form_validation_for_blank_input(self):
        form = ArticleForm(data={"title": ""})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["title"], [EMPTY_ARTICLE_ERROR])


if __name__ == "__main__":
    pass
