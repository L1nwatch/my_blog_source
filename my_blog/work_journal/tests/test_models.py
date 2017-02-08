#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.02.07 需要给日记添加日期, 进行测试
2017.02.03 新建了 MODEL, 虽然不知道要测试啥, 就简单写个字段测试吧
"""
import datetime

from django.test import TestCase
from work_journal.models import Journal

__author__ = '__L1n__w@tch'


class JournalModelTest(TestCase):
    def test_journal_model_has_title_and_content(self):
        new_journal = Journal.objects.create(title="test_journal_1",
                                             content="test_journal_content_1", date=datetime.date.today())
        self.assertEqual(new_journal.title, "test_journal_1")
        self.assertEqual(new_journal.content, "test_journal_content_1")

    def test_create_time_equal_to_update_time_when_create_new_article(self):
        """
        新建一篇文章时, 应该带有对应的日记日期
        :return:
        """
        right_date = datetime.date(2017, 2, 3)
        new_journal = Journal.objects.create(title="2017-02-03-任务情况总结", content="test", date=right_date)
        journal_date = new_journal.date
        self.assertEqual(journal_date, right_date)


if __name__ == "__main__":
    pass
