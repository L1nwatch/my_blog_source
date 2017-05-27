#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.05.27 补充 ConfigInteractive 的相关测试
2017.04.30 修正测试, 加入到 django 测试框架中, 补充没写的 test_do_nothing_when_exist
2016.10.19 编写单元测试, 测试自己的代码能否正确修改 /etc/crontab 文件
"""
# 自己的模块
from fabfile import _update_setting_to_conf_file, ConfigInteractive
import my_constant

# 标准库
import os
import re
import configparser
import io
import sys
from collections import namedtuple

from django.test import TestCase
from django.conf import settings
from importlib import reload

__author__ = '__L1n__w@tch'


class BaseFabfileTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.current_dir_name = os.path.dirname(__file__)
        cls.base_dir = os.path.dirname(cls.current_dir_name)


class TestModifyCrontabFile(BaseFabfileTest):
    def setUp(self):
        super(TestModifyCrontabFile, self).setUp()
        self.test_file_name = os.path.join(self.base_dir, self.current_dir_name, "for_test_crontab.txt")

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
        new_content = str().join(_update_setting_to_conf_file(old_content, "manage.py runcrons --force"))
        self.assertIn("manage.py runcrons --force", new_content)

    def test_do_nothing_when_exist(self):
        """
        已经存在相应配置则不改动
        :return:
        """
        # 一开始已经有配置行了
        with open(self.test_file_name, "r") as f:
            old_content = f.readlines()
        old_content.insert(-1, "manage.py runcrons --force")
        self.assertIn("manage.py runcrons --force", old_content)

        # 运行完函数之后内容不变
        new_content = _update_setting_to_conf_file(old_content, "manage.py runcrons --force")
        self.assertTrue(
            all(
                [x.strip() == y.strip() for x, y in zip(old_content, new_content)]
            )
        )


class TestGitBookConf(BaseFabfileTest):
    def setUp(self):
        super(TestGitBookConf, self).setUp()

        self.gitbook_conf_name = "gitbooks_git.conf"
        self.test_file_name = os.path.join(self.base_dir, self.current_dir_name, self.gitbook_conf_name)
        self.const_file_path = os.path.join(settings.BASE_DIR, "my_constant.py")

        # 保存原来的文件
        with open(self.const_file_path, "rb") as f:
            self.old_content = f.read()

        # 调用函数, 将 Conf 中的内容应用到文件中去
        self.update_const_file()

    def update_const_file(self):
        print("[*] 即将读取 {} 下的 gitbooks 路径".format(self.gitbook_conf_name))

        # 读取文件内容
        with open(self.test_file_name, "r") as f:
            data = f.read()

        # 通过 re 修改 const 文件
        with open(self.const_file_path, "r") as f:
            raw_git_data = f.read()
        raw_git_data = re.sub('const\.GITBOOK_CODES_REPOSITORY = \{[^}]*\}',
                              'const.GITBOOK_CODES_REPOSITORY = {}'.format(data), raw_git_data)

        with open(self.const_file_path, "w") as f:
            f.write(raw_git_data)

        print("[*] 成功将 {} 中的 gitbooks 路径更新到配置文件中".format(self.gitbook_conf_name))

    def tearDown(self):
        # 恢复原来的文件
        with open(self.const_file_path, "wb") as f:
            f.write(self.old_content)

        super(TestGitBookConf, self).tearDown()

    def test_gitbook_conf_format_is_right(self):
        """
        测试 gitbook_conf 文件的格式是正确的
        :return:
        """
        reload(my_constant)
        my_answer = my_constant.const.GITBOOK_CODES_REPOSITORY

        for each_book in my_answer:
            # 首先得是个命名元组
            self.assertIsInstance(my_answer[each_book], my_constant.const.GITBOOK_INFO)

            # 然后包含有 git_address 属性, 之后要符合 git 的格式
            self.assertIsNotNone(my_answer[each_book].git_address)
            self.assertRegex(my_answer[each_book].git_address, "^https?://.+\.git$")

            # 以及包含有 book_name 属性, 书名用 《》 括起来
            self.assertIsNotNone(my_answer[each_book].book_name)
            self.assertRegex(my_answer[each_book].book_name, "^《.+》$")


class TestConfigInteractive(BaseFabfileTest):
    @classmethod
    def setUpClass(cls):
        cls.config_structure = namedtuple("config_structure", ("section", "option"))

        # 配置文件所包含的配置项
        cls.test_config_file_path = "test_config.conf"
        cls.ci = ConfigInteractive(cls.test_config_file_path)

        super().setUpClass()

    def setUp(self):
        """
        创建测试用的配置文件
        """
        cp = configparser.ConfigParser()

        # 创建 section 及对应的 option
        for each_config in self.ci.sections_options:
            if not cp.has_section(each_config.section):
                cp.add_section(each_config.section)
            if not cp.has_option(each_config.section, each_config.option):
                cp.set(each_config.section, each_config.option, str())

        with open(self.test_config_file_path, "w") as f:
            cp.write(f)

    def tearDown(self):
        """
        删除测试用的 conf 文件
        """
        if os.path.exists(self.test_config_file_path):
            os.remove(self.test_config_file_path)

    def read_config_file(self):
        cp = configparser.ConfigParser()
        cp.read(self.test_config_file_path)
        return cp

    def test_config_can_update_when_has_new_option(self):
        """
        创建当配置文件存在时, 如果某些字段不存在于配置文件中, 则配置文件会对这些字段进行更新
        """
        # 添加某个字段
        test_section, test_option = "test_section", "test_option"

        self.ci.sections_options.append(self.config_structure(test_section, test_option))

        # 验证当前配置文件中不存在某个字段
        cp = self.read_config_file()
        with self.assertRaises(configparser.NoSectionError):
            cp.get(test_section, test_option)

        # 调用创建配置文件的函数
        self.ci._create_config_file()

        # 发现最新的字段已经被添加进来了, 且设置了默认值空值
        cp = self.read_config_file()
        self.assertEqual(cp.get(test_section, test_option), str())

    def test_can_set_option_correct(self):
        """
        测试可以正确设置字段值到配置文件中
        """
        # 确保当前所有字段值为空
        cp = self.read_config_file()
        for each_config in self.ci.sections_options:
            self.assertEqual(cp.get(each_config.section, each_config.option), str())

        # 为每一个字段进行赋值
        config_data_string = io.StringIO("\n".join(["a" * (i + 1) for i in range(len(self.ci.sections_options))]))

        old_sys_stdin, sys.stdin = sys.stdin, config_data_string
        self.ci.user_pass_file_config()
        sys.stdin = old_sys_stdin

        # 验证每个字段的值都是正确的
        cp = self.read_config_file()
        for i, each_config in enumerate(self.ci.sections_options):
            self.assertEqual(cp.get(each_config.section, each_config.option), "a" * (i + 1))


if __name__ == "__main__":
    pass
