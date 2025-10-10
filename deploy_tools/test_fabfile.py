#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""

2017.06.16 需要给 GitBook 添加 Tag 标签, 因此更改 conf 的测试代码 + 完善测试 gitbook conf 的代码
2017.06.08 由于重构了常量脚本, 因此重构对应测试 + 根据部署脚本的更改修改对应测试
2017.05.28 补充更新配置文件的测试代码
2017.05.28 改成 unittest.TC 了, 因为 django.test 没法测试到这边的。。。
2017.05.27 补充 ConfigInteractive 的相关测试
2017.04.30 修正测试, 加入到 django 测试框架中, 补充没写的 test_do_nothing_when_exist
2016.10.19 编写单元测试, 测试自己的代码能否正确修改 /etc/crontab 文件
"""
# 自己的模块
from .fabfile import _update_setting_to_conf_file, ConfigInteractive, UpdateConfigFile
import my_constant

# 标准库
import os
import configparser
import io
import sys
import unittest
import unittest.mock
import re
import subprocess
from collections import namedtuple

from django.conf import settings

__author__ = '__L1n__w@tch'


class BaseFabfileTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.current_dir_name = os.path.dirname(__file__)  # 当前文件夹名字
        cls.base_dir = os.path.dirname(cls.current_dir_name)  # 根文件夹路径


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


class TestConfigInteractive(BaseFabfileTest):
    test_config_file_path = "test_config.conf"

    @classmethod
    def setUpClass(cls):
        cls.config_structure = namedtuple("config_structure", ("section", "option"))

        # 配置文件所包含的配置项
        cls.ci = ConfigInteractive(cls.test_config_file_path)

        super().setUpClass()

    def setUp(self):
        """
        创建测试用的配置文件
        """
        self.create_user_pass_config_file()

    def create_user_pass_config_file(self):
        cp = configparser.ConfigParser()

        # 创建 section 及对应的 option
        for each_config in self.ci.sections_options:
            if not cp.has_section(each_config.section):
                cp.add_section(each_config.section)
            if not cp.has_option(each_config.section, each_config.option):
                cp.set(each_config.section, each_config.option, str())

        with open(self.test_config_file_path, "w") as f:
            cp.write(f)

    def delete_user_pass_config_file(self):
        if os.path.exists(self.test_config_file_path):
            os.remove(self.test_config_file_path)

    def tearDown(self):
        """
        删除测试用的 conf 文件
        """
        self.delete_user_pass_config_file()

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
        config_data_string = io.StringIO("\n".join(["1" * (i + 1) for i in range(len(self.ci.sections_options))]))

        old_sys_stdin, sys.stdin = sys.stdin, config_data_string
        self.ci.user_pass_file_config()
        sys.stdin = old_sys_stdin

        # 验证每个字段的值都是正确的
        cp = self.read_config_file()
        for i, each_config in enumerate(self.ci.sections_options):
            self.assertEqual(cp.get(each_config.section, each_config.option), "1" * (i + 1))


class TestUpdateConfigFile(BaseFabfileTest):
    def setUp(self):
        super().setUp()

        self.gitbook_conf_path = os.path.join(self.current_dir_name, "gitbooks_git.conf")
        self.my_constant_py_path = os.path.join(settings.BASE_DIR, "my_constant.py")
        self.user_pass_config_file_path = os.path.join(self.current_dir_name, "test_config.conf")
        self.settings_py_path = os.path.join(settings.BASE_DIR, "my_blog", "settings.py")
        self.ucf = UpdateConfigFile(source_folder=self.base_dir, site_name="my_blog", host_name="127.0.0.1")

        # 保存原来 my_constant.py 中的内容
        with open(self.my_constant_py_path, "rb") as f:
            self.my_constant_py_old_content = f.read()

    def tearDown(self):
        # 恢复 my_constant.py 中的内容
        with open(self.my_constant_py_path, "wb") as f:
            f.write(self.my_constant_py_old_content)

    def test_update_gitbooks_config(self):
        """
        测试将 GitBook 链接更新到 my_constant.py 文件中
        """

        with open(self.gitbook_conf_path, "r") as f:
            conf_data = f.read()

        already_present = conf_data.encode() in self.my_constant_py_old_content

        # 调用更新操作
        self.ucf.update_gitbooks_config(self.gitbook_conf_path, self.my_constant_py_path)

        # 发现 conf 文件里面的内容都存在于 py 文件中了
        with open(self.my_constant_py_path, "r") as f:
            my_constant_py_new_content = f.read()
        self.assertIn(conf_data, my_constant_py_new_content)

        if not already_present:
            self.assertNotIn(conf_data.encode(), self.my_constant_py_old_content)

        # 而且格式是正确的
        self.test_gitbook_conf_format_is_right()

        # 并且是位于 const.GITBOOK_CODES_REPOSITORY 的花括号之间
        pattern = "const.GITBOOK_CODES_REPOSITORY = (\{.*?\})"
        re_result = re.findall(pattern, my_constant_py_new_content, flags=re.IGNORECASE | re.DOTALL)[0]
        self.assertEqual(re_result.strip(), conf_data.strip())

    def test_gitbook_conf_format_is_right(self):
        """
        测试 gitbook_conf 文件的格式是正确的
        """
        global my_constant
        del sys.modules["my_constant"]
        del my_constant
        import my_constant
        my_answer = my_constant.GITBOOK_CODES_REPOSITORY

        for each_book in my_answer:
            # 首先得是个命名元组
            self.assertIsInstance(my_answer[each_book], my_constant.GITBOOK_INFO)

            # 然后包含有 git_address 属性, 之后要符合 git 的格式
            self.assertIsNotNone(my_answer[each_book].git_address)
            self.assertRegex(my_answer[each_book].git_address, r"^(?:https?://.+\.git|git@.+:.+\.git)$")

            # 以及包含有 book_name 属性, 书名用 《》 括起来
            self.assertIsNotNone(my_answer[each_book].book_name)
            self.assertRegex(my_answer[each_book].book_name, "^《.+》$")

            # 还要有 Tag 属性, 可以为空列表, 或者多个标签等
            self.assertIsInstance(my_answer[each_book].tag_names, list)

    def test_update_const_config(self):
        """
        测试能够将 journal 的相关配置以及 article 的相关配置更新到 my_constant.py 中去
        """
        # 创建 user_pass 的测试文件
        test_input = self.create_user_pass_test_file()
        test_username, test_password = test_input["username"], test_input["password"]
        test_address = test_input["address"]

        try:
            # 原本几个测试数据都不存在于配置文件中
            for x in (test_username, test_password, test_address):
                self.assertNotIn(x.encode(), self.my_constant_py_old_content)

            # 调用更新函数
            self.ucf.update_user_pass_config(self.user_pass_config_file_path, self.my_constant_py_path)

            # 现在几个测试数据都存在于配置文件中了
            with open(self.my_constant_py_path, "r") as f:
                my_constant_py_content = f.read()
            for x in (test_username, test_password, test_address):
                self.assertIn(x, my_constant_py_content)

            # 并且存在于对应的项中
            pattern = "const.JOURNALS_GIT_REPOSITORY = \"(.*)\""
            re_result = re.findall(pattern, my_constant_py_content, flags=re.IGNORECASE)
            right_answer = "https://{}:{}@git.oschina.net/w4tch/sxf_notes_set.git".format(test_username, test_password)
            self.assertEqual(re_result[0], right_answer)

            pattern = "const.ARTICLES_GIT_REPOSITORY = \"(.*)\""
            re_result = re.findall(pattern, my_constant_py_content, flags=re.IGNORECASE)
            self.assertEqual(re_result[0], test_address)
        finally:
            # 删除 user_pass 的测试文件
            if os.path.exists(self.user_pass_config_file_path):
                os.remove(self.user_pass_config_file_path)

    def create_user_pass_test_file(self):
        """
        创建 user_pass.conf 文件以供测试
        """
        result = dict()

        result["username"] = "测试用的用户名"
        result["password"] = "测试用的密码"
        result["address"] = "测试用的地址"
        result["smtp_password"] = "SMTP 密码"
        result["smtp_user"] = "SMTP 用户名"
        result["smtp_server_host"] = "服务器主机地址"
        result["smtp_server_port"] = 12306

        test_content = """
[journals_git]
username = {username}
password = {password}

[articles_git]
address = {address}

[email_info]
smtp_password = {smtp_password}
smtp_user = {smtp_user}
smtp_server_host = {smtp_server_host}
smtp_server_port = {smtp_server_port}
""".format(username=result["username"], password=result["password"], address=result["address"],
           smtp_password=result["smtp_password"], smtp_server_host=result["smtp_server_host"],
           smtp_user=result["smtp_user"], smtp_server_port=result["smtp_server_port"])

        with open(self.user_pass_config_file_path, "w") as f:
            f.write(test_content)

        return result

    def test_update_settings(self):
        """
        测试能否更新 settings.py 文件, 主要是把 email 配置写入, 还有 DEBUG、DOMAIN 等字段的调整
        """

        def __my_sed(file_path, raw_string, new_string):
            """
            自己实现的 sed 函数
            """
            call_result = subprocess.check_output(
                ["sed", "-e", "s/{}/{}/g".format(raw_string, new_string), file_path])

            with open(file_path, "wb") as f:
                f.write(call_result)

        # 备份 settings.py 文件
        with open(self.settings_py_path, "rb") as f:
            settings_old_content = f.read()

        # 创建 USER_PASS 测试文件, 提供 email 配置信息
        test_data = self.create_user_pass_test_file()

        try:
            # 原本几个 email 字段(除了 PORT 字段)的内容都不在 settings.py 中
            for each_email_info in ("smtp_password", "smtp_user", "smtp_server_host"):
                self.assertNotIn(test_data[each_email_info].encode(), settings_old_content)

            # 调用更新函数
            with unittest.mock.patch("deploy_tools.fabfile.sed", side_effect=__my_sed) as my_sed, \
                    unittest.mock.patch("deploy_tools.fabfile.exists") as my_exists, \
                    unittest.mock.patch("deploy_tools.fabfile.append") as my_append:
                self.ucf.update_settings(self.settings_py_path, self.user_pass_config_file_path)

            # 重新读取文件内容
            with open(self.settings_py_path, "r") as f:
                new_settings_content = f.read()

            patterns = ["EMAIL_HOST = \"(.*)\"", "EMAIL_PORT = (\d+)", "EMAIL_HOST_USER = \"(.*)\"",
                        "EMAIL_HOST_PASSWORD = \"(.*)\""]
            fields = ["smtp_server_host", "smtp_server_port", "smtp_user", "smtp_password"]
            for pattern, each_field in zip(patterns, fields):
                # 检查更新是否成功, 发现这几个字段都出现在文件中了
                self.assertTrue(str(test_data[each_field]) in new_settings_content,
                                msg="[-] 关键词: '{}' 不在内容中".format(test_data[each_field]))

                # 并且存在于对应的项中
                re_result = re.findall(pattern, new_settings_content, flags=re.IGNORECASE)
                self.assertEqual(re_result[0], str(test_data[each_field]),
                                 msg="[-] 找不到: {}".format(test_data[each_field]))
        finally:
            # 恢复 settings.py 文件的内容
            with open(self.settings_py_path, "wb") as f:
                f.write(settings_old_content)

            # 删除 user_pass 的测试文件
            if os.path.exists(self.user_pass_config_file_path):
                os.remove(self.user_pass_config_file_path)


if __name__ == "__main__":
    pass
