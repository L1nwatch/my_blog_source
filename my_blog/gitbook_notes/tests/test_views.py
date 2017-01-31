#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 测试 gitbook_notes 这个 app 下的视图函数

2017.01.28 增加了测试完毕之后删除测试文件夹的代码
2016.10.30 对更新笔记的视图函数进行测试
"""
from django.test import TestCase, override_settings
from my_constant import const

import os
import unittest
import shutil

__author__ = '__L1n__w@tch'


@override_settings(UPDATE_TIME_LIMIT=0.1)
@unittest.skipUnless(const.SLOW_CONNECT_DEBUG, "const.SLOW_CONNECT_DEBUG 值为 True 才表示要进行 git 测试")
class UpdateGitBookCodesViewTest(TestCase):
    unique_url = "/gitbook_notes/update_gitbook_codes/"
    gitbook_category_dict = const.GITBOOK_CODES_REPOSITORY
    notes_git_path = const.GITBOOK_CODES_PATH

    def test_can_get_md_from_git(self):
        """
        测试能从 gitbook 的各个仓库中获取到 gitbook 的源码
        :return:
        """
        # 点击更新按钮
        self.client.get(self.unique_url)

        # 发现更新成功了, 每个文件夹都存在, 而且其文件夹下还有 .git
        for each_gitbook_name in self.gitbook_category_dict:
            self.assertTrue(os.path.exists(os.path.join(self.notes_git_path, each_gitbook_name, ".git")), "找不到 .git")

    def tearDown(self):
        # 清楚 git clone 到的文件
        if os.path.exists(self.notes_git_path):
            shutil.rmtree(self.notes_git_path)


if __name__ == "__main__":
    pass
