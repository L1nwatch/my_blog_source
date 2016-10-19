#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2016.10.19 编写单元测试, 测试自己的代码能否正确修改 /etc/crontab 文件
"""
import unittest
from fabfile import _update_setting_to_conf_file

__author__ = '__L1n__w@tch'


class TestModifyCrontabFile(unittest.TestCase):
    def setUp(self):
        self.test_file_name = "for_test_crontab.txt"

    def test_add_new_line_when_no_exist(self):
        """
        测试是否能够成功给一个没有相应配置行的文件添加一个配置行
        :return:
        """
        # 一开始是没有配置行的
        with open(self.test_file_name, "r") as f:
            old_content = f.readlines()
        self.assertNotIn("manage.py runcrons --force", old_content)

        # 运行完函数之后就有了配置行了
        new_content = str().join(_update_setting_to_conf_file(old_content))
        self.assertIn("manage.py runcrons --force", new_content)

    def test_do_nothing_when_exist(self):
        """
        已经存在相应配置则不改动
        :return:
        """
        pass


if __name__ == "__main__":
    pass
