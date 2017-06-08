#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.02.03 添加了 JournalForm 后要进行测试
"""

from work_journal.forms import JournalForm
from django.test import TestCase
import my_constant as const

__author__ = '__L1n__w@tch'


class JournalFormTest(TestCase):
    def test_form_item_input_has_placeholder_and_css_classes(self):
        """
        测试表单是否包含了 PLACE_HOLDER/class/id 属性
        :return:
        """
        journal_form = JournalForm()
        self.assertIn('placeholder="{}"'.format(const.PLACE_HOLDER), journal_form.as_p())
        self.assertIn('class="pure-input-2-3"', journal_form.as_p(), "class 属性没有设置?还是说设置错了?")
        self.assertIn('id="id_search_work_journal"', journal_form.as_p(), "id 属性没有设置?还是说设置错了?")

    def test_form_validation_for_blank_input(self):
        form = JournalForm(data={"search_content": "", "search_choice": "journals"})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["search_content"], [const.EMPTY_ARTICLE_ERROR])


if __name__ == "__main__":
    pass
