#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.04.30 修正测试, 加入到 django 测试框架中, 补充没写的 test_do_nothing_when_exist
2016.10.19 编写单元测试, 测试自己的代码能否正确修改 /etc/crontab 文件
"""
import os
import re

from fabfile import _update_setting_to_conf_file
import my_constant

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


if __name__ == "__main__":
    pass
