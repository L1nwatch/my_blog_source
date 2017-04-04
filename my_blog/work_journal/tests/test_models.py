#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 负责 work_journal 的 Model 测试

2017.04.04 重构创建测试数据相关的代码
2017.02.07 需要给日记添加日期, 进行测试
2017.02.03 新建了 MODEL, 虽然不知道要测试啥, 就简单写个字段测试吧
"""
import datetime

from articles.tests.basic_test import BasicTest

__author__ = '__L1n__w@tch'


class JournalModelTest(BasicTest):
    def test_journal_model_has_title_and_content(self):
        new_journal = self.create_journal(title="test_journal_1", content="test_journal_content_1")
        self.assertEqual(new_journal.title, "test_journal_1")
        self.assertEqual(new_journal.content, "test_journal_content_1")

    def test_create_time_equal_to_update_time_when_create_new_article(self):
        """
        新建一篇文章时, 应该带有对应的日记日期
        :return:
        """
        right_date = datetime.date(2017, 2, 3)
        new_journal = self.create_journal(date=right_date)
        journal_date = new_journal.date
        self.assertEqual(journal_date, right_date)


if __name__ == "__main__":
    pass
