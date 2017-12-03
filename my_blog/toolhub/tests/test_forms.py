#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 为 toolhub 下的 form 进行相关测试

2017.03.25 新增 GitHub 图片地址转换器 form 的相关测试
"""
from django.test import TestCase
from toolhub.forms import GitHubTranslateTextareaForm

__author__ = '__L1n__w@tch'


class JournalFormTest(TestCase):
    def test_form_item_input_has_attributes(self):
        """
        测试表单是否包含了 PLACE_HOLDER/spellcheck/id  等属性
        :return:
        """
        input_form = GitHubTranslateTextareaForm()
        self.assertIn("autofocus", input_form.as_p())
        self.assertIn('id="id_input_box"', input_form.as_p(), "id 属性没有设置?还是说设置错了?")
        self.assertIn('placeholder="请输入你要转换的数据"', input_form.as_p(), "没有设置 placeholder?")

