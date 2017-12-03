#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""  对 log_file_deal 模块进行测试

2017.06.03 修改 log 打包后的名字, 主要是补充 0 位
2017.05.28 修正继承类, 使其可以跟 Django Test All 一起
2017.05.20 测试 log_packer 是否进行正常打包工作
"""
# 标准库
import os
import zipfile
import datetime
from django.test import TestCase

# 自己的模块
from log_file_deal.log_packer import LogPacker

__author__ = '__L1n__w@tch'


class TestLogPacker(TestCase):
    def setUp(self):
        self.lp = LogPacker(os.curdir)
        self.test_file_names = ["a", "b", "c"]

        # 创建测试用的 log 文件
        for file_name in self.test_file_names:
            with open("{}.log".format(file_name), "w") as f:
                f.write("{}".format(file_name * 30))

        self.today = datetime.datetime.today()
        self.yesterday = self.today - datetime.timedelta(days=1)
        self.log_zip_name = "{}{}{}_log.zip".format(self.yesterday.year,
                                                    str(self.yesterday.month).zfill(2),
                                                    str(self.yesterday.day).zfill(2))

    def tearDown(self):
        # 删除测试用的 log 文件
        for file_name in self.test_file_names:
            os.remove("{}.log".format(file_name))

        # 删除测试生成的 zip 文件
        if os.path.exists(self.log_zip_name):
            os.remove(self.log_zip_name)

    @staticmethod
    def un_zip(file_path):
        """
        解压 zip 文件
        :param file_path: str(), gz 文件路径
        :return: str(), 从 zip 提取出来的所有文件的文件名
        """
        if zipfile.is_zipfile(file_path):
            with zipfile.ZipFile(file_path, "r") as my_zip:
                my_zip.extractall()
        else:
            raise RuntimeError("[-] {} 不是标准的 ZIP 文件".format(file_path))

    def test_run(self):
        # 原本不存在 日期_log.zip 的压缩包
        self.assertFalse(os.path.exists(self.log_zip_name))

        self.lp.run()

        # run 操作执行完后, 应该存在一个 日期_log.gz 的压缩包
        self.assertTrue(os.path.exists(self.log_zip_name))

        # 而且原来的 log 文件里面的内容全都被清空了
        for file_name in self.test_file_names:
            with open("{}.log".format(file_name), "r") as f:
                self.assertEqual(str(), f.read())
            # 删除所有 log 文件
            os.remove("{}.log".format(file_name))
            self.assertFalse(os.path.exists("{}.log".format(file_name)))

        # 解压压缩包
        self.un_zip(self.log_zip_name)

        # 原来的 log 文件内容存在于解压后的文件内容之中
        for file_name in self.test_file_names:
            with open("{}.log".format(file_name), "r") as f:
                self.assertEqual("{}".format(file_name * 30), f.read())

