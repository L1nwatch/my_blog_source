#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.02.03 新建了 MODEL, 虽然不知道要测试啥, 就简单写个字段测试吧
"""
from django.test import TestCase
from work_journal.models import Journal

__author__ = '__L1n__w@tch'


class JournalModelTest(TestCase):
    def test_journal_model_has_title_and_content(self):
        new_journal = Journal.objects.create(title="test_journal_1", content="test_journal_content_1")
        self.assertEqual(new_journal.title, "test_journal_1")
        self.assertEqual(new_journal.content, "test_journal_content_1")


if __name__ == "__main__":
    pass
