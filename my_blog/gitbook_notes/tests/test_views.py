#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 测试 gitbook_notes 这个 app 下的视图函数

2016.10.30 对更新笔记的视图函数进行测试
"""
from django.conf import settings
from django.test import TestCase, override_settings
from my_constant import const

import os
import unittest

__author__ = '__L1n__w@tch'


@override_settings(UPDATE_TIME_LIMIT=0.1)
@unittest.skipUnless(const.SLOW_CONNECT_DEBUG, "值为 True 表示要进行 git 测试")
class UpdateGitBookCodesViewTest(TestCase):
    unique_url = "/gitbook_notes/update_notes/"
    notes_path_name = "gitbook_notes"
    gitbook_category_list = list()

    notes_path_parent_dir = os.path.dirname(settings.BASE_DIR)
    notes_git_path = os.path.join(notes_path_parent_dir, notes_path_name)

    def test_can_get_md_from_git(self):
        """
        测试能从 gitbook 的各个仓库中获取到 gitbook 的源码
        :return:
        """
        print("测试 gitbook notes 了")
        pass


if __name__ == "__main__":
    pass
