#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.12.03 为新增的一个判断合法 IP 的函数作测试
2017.06.10 添加日志记录的字段, 现在还会添加 UserAgent 等 HTTP 头的信息了 + 只获取指定的 HTTP 头字段
2017.06.04 重构搜索结果数据结构, 因此更改对应测试代码 + 添加一个测试解析 tag 的函数
2017.06.03 修正笔记数的获取方式, 换了一个好像更高效的方法来统计
2017.06.03 继续重写代码逻辑, 避免数据库锁定以及发邮件卡顿的问题, 于是修改对应测试代码
2017.06.02 优化排序代码, 更改对应测试代码, 新增一个更新笔记数的函数
2017.05.26 补充 log 的测试
2017.05.21 将该文件移到共同测试模块
2017.04.30 新增有关 git 地址的测试代码
2017.03.26 新增有关搜索输入的测试代码
2017.03.23 新增有关搜索结果排序的测试
2017.03.07 为共有函数进行测试编写
"""
# 自己的模块
from common_module.common_help_function import (clean_form_data, sort_search_result, locate_using_ip_address,
                                                data_check, is_valid_git_address, background_deal, model_dict,
                                                extract_tag_name_from_path, get_http_header_from_request, is_valid_ip)
import my_constant as const
from .basic_test import BasicTest

# 标准库
import random
import string
import unittest.mock
import re

from django.test.client import RequestFactory

__author__ = '__L1n__w@tch'


class TestCommonHelpFunc(BasicTest):
    def test_clean_form_data(self):
        # 测试 "aa ", 应该得到 "aa"
        test_data = "aa "
        right_answer = "aa"
        my_answer = clean_form_data(test_data)
        self.assertEqual(right_answer, my_answer)

        # 测试 "aa bb", 应该得到 "aa bb"
        test_data = "aa bb"
        right_answer = "aa bb"
        my_answer = clean_form_data(test_data)
        self.assertEqual(right_answer, my_answer)

        # 测试 " bb", 应该得到 "bb"
        test_data = " bb"
        right_answer = "bb"
        my_answer = clean_form_data(test_data)
        self.assertEqual(right_answer, my_answer)

        # 测试 "test_article", 应该得到 "test_article"
        test_data = "test_article "
        right_answer = "test_article"
        my_answer = clean_form_data(test_data)
        self.assertEqual(right_answer, my_answer)

    def test_sort_search_result(self):
        """
        测试排序结果的函数是否排序正确
        """
        test_article1 = self.create_article(click_times=1)
        test_article2 = self.create_article(click_times=3)
        test_article3 = self.create_article(click_times=2)

        test_result_list = [
            const.ARTICLE_STRUCTURE(test_article1, "aa", "articles"),
            const.ARTICLE_STRUCTURE(test_article2, "bb", "articles"),
            const.ARTICLE_STRUCTURE(test_article3, "cc", "articles"),
        ]
        right_answer = [
            const.ARTICLE_STRUCTURE(test_article2, "bb", "articles"),
            const.ARTICLE_STRUCTURE(test_article3, "cc", "articles"),
            const.ARTICLE_STRUCTURE(test_article1, "aa", "articles"),
        ]
        my_answer = sort_search_result(test_result_list)
        self.assertEqual(len(my_answer), 3)
        for each_right, each_mine in zip(right_answer, my_answer):
            self.assertEqual(each_right, each_mine)

    def test_data_check(self):
        # 单个字符(仅限英文、数字、特殊字符)的输入, 都认为非法
        # 单个中文
        test_data = "啊"
        self.assertTrue(data_check(test_data))

        # 单个非中文
        for each_char in string.printable:
            self.assertFalse(data_check(each_char))

        # 多个字符, 如果全是特殊字符, 则认为非法
        # 含非特殊字符
        for i in range(100):
            test_data = random.choice(string.ascii_letters + string.digits) + "".join(
                [random.choice(string.punctuation) for j in range(random.randint(2, 30))])
            self.assertTrue(data_check(test_data))

        # 不含非特殊字符
        for i in range(100):
            test_data = "".join([random.choice(string.punctuation) for j in range(random.randint(2, 100))])
            self.assertFalse(data_check(test_data))

    def test_is_valid_git_address(self):
        test_data = "https://xxx.git"
        my_answer = is_valid_git_address(test_data)
        self.assertTrue(my_answer)

        test_data = "https://www.baidu.com"
        my_answer = is_valid_git_address(test_data)
        self.assertFalse(my_answer)

        test_data = "https://xxx.git.com"
        my_answer = is_valid_git_address(test_data)
        self.assertFalse(my_answer)

    def test_can_log_data(self):
        """
        测试日志记录, 有发送邮件的记录, 还有 IP 地址、时间、HTTP 头的记录
        :return:
        """
        rf = RequestFactory()
        get_request = rf.get("/")

        with unittest.mock.patch("articles.views.logger") as log_mock, unittest.mock.patch(
                "django.core.mail.send_mail") as email_sender:
            background_deal(logger=log_mock, level="info", request=get_request, func_kwargs=dict(),
                            str_format=str(), ip_address="11.11.11.11", email_check=True)

            method_calls = log_mock.method_calls

            # 有发送邮件的记录
            self.assertTrue(any(
                ['[*] 开始尝试发送邮件' == x[1][0] for x in method_calls]
            ))

            # 有 IP 以及时间信息
            ip_time_re = re.compile("\[\*\].*IP \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} 于 \d{4}-\d{2}-\d{2}",
                                    flags=re.IGNORECASE)

            self.assertTrue(any([ip_time_re.match(x[1][0]) for x in method_calls]))

            # HTTP 头的记录
            self.assertTrue(any("QUERY_STRING" in x[1][0] for x in method_calls))

    def test_can_log_data_while_visit_home(self):
        """
        测试通过客户端访问首页会记录日志
        """
        with unittest.mock.patch("common_module.email_send.email_sender.send_email") as send_email_mock:
            # 通过客户端访问首页
            self.client.get("/")

            # 日志记录中的发邮件函数被触发
            self.assertTrue(send_email_mock.called)

    def test_will_send_email_when_new_ip_visit(self):
        """
        测试当有新 IP 访问时会执行发送邮件的操作
        """
        # 前置条件设置, 确保是一个新的 IP, 并且对发送邮件函数进行 mock 操作
        with unittest.mock.patch("common_module.email_send.email_sender.want_to_send_email") as send_check, \
                unittest.mock.patch("common_module.email_send.email_sender.try_to_send_email") as send_email:
            send_check.return_value = True

            # 存在一个访问请求, 访问首页
            self.client.get("/")

            # 确认两个函数都被调用了
            self.assertTrue(send_check.called)
            self.assertTrue(send_email.called)

    @unittest.skipUnless(const.SLOW_CONNECT_DEBUG, "[*] 忽略部分耗时测试")
    def test_locate_using_ip_address(self):
        """
        测试通过 IP 定位地理信息是否正确
        """
        my_answer = locate_using_ip_address("66.249.79.71")
        right_answer = "美国"
        self.assertEqual(right_answer, my_answer)

        my_answer = locate_using_ip_address("88.198.54.49")
        right_answer = "德国"
        self.assertEqual(right_answer, my_answer)

        my_answer = locate_using_ip_address("113.140.11.123")
        right_answer = "中国-西安市"
        self.assertEqual(right_answer, my_answer)

        my_answer = locate_using_ip_address("127.0.0.1")
        right_answer = "内网 IP"
        self.assertEqual(right_answer, my_answer)

    def test_update_notes_number(self):
        """
        验证获取统计数的方法是正确
        """
        # 新增了笔记
        for types in ("articles", "journals", "gitbooks"):
            create_func = self.create_func_map(types)
            # 创建 3 篇笔记
            for i in range(3):
                create_func()

            # 检查笔记数的统计是否正确
            for key, value in model_dict.items():
                self.assertEqual(value.objects.all().count(), len(value.objects.all()))

    def test_extract_tag_name_from_path(self):
        # 含 2 个目录
        test_data = ('/Users/L1n/Desktop/Code/Python/my_blog_source/notes',
                     '/Users/L1n/Desktop/Code/Python/my_blog_source/notes/aa/bb/总结笔记-Docker学习.md')
        right_answer = ["aa", "bb"]
        my_answer = extract_tag_name_from_path(*test_data)
        self.assertEqual(right_answer, my_answer)

        # 根目录
        test_data = ('/Users/L1n/Desktop/Code/Python/my_blog_source/notes',
                     '/Users/L1n/Desktop/Code/Python/my_blog_source/notes/总结笔记-Docker学习.md')
        right_answer = list()
        my_answer = extract_tag_name_from_path(*test_data)
        self.assertEqual(right_answer, my_answer)

        # 只含 1 个目录
        test_data = ('/Users/L1n/Desktop/Code/Python/my_blog_source/notes',
                     '/Users/L1n/Desktop/Code/Python/my_blog_source/notes/aa/总结笔记-Docker学习.md')
        right_answer = ["aa"]
        my_answer = extract_tag_name_from_path(*test_data)
        self.assertEqual(right_answer, my_answer)

    def test_get_http_header_from_request(self):
        """
        测试从 request 中获取 http 头部信息正常
        """
        rf = RequestFactory()
        get_request = rf.get("/", HTTP_USER_AGENT="Mozilla")

        http_info = get_http_header_from_request(request=get_request)

        # 仅仅测试 QUERY_STRING 字段, 由于 request 是伪造的, 所以其他 HTTP 字段不存在
        self.assertIn("QUERY_STRING", http_info)
        self.assertIn("HTTP_USER_AGENT", http_info)

    def test_get_http_header_from_request_only_return_pointed_field(self):
        """
        测试只获取 HTTP 头中指定的字段, 其他字段不获取
        """
        rf = RequestFactory()
        get_request = rf.get("/")

        http_info = get_http_header_from_request(request=get_request)

        # 只希望获取到指定的 5 个字段, 包括 QUERY_STRING/SERVER_PORT/REQUEST_METHOD/SERVER_NAME/REMOTE_ADDR
        http_info = http_info.splitlines()
        self.assertEqual(len(http_info), 5)
        for each_field in http_info:
            each_field = each_field.split(" -> ")[0]
            self.assertIn(each_field, const.LOG_HTTP_HEADERS_WHITE_LIST)

    def test_is_valid_ip(self):
        """
        判断是否合法 IP 成功
        :return:
        """
        # 测试默认值
        self.assertTrue(is_valid_ip("127.0.0.1"))

        # 测试解析
        self.assertTrue(is_valid_ip("127.0.0.1", ip_list=["localhost"]))
        self.assertTrue(is_valid_ip("216.24.184.200", ip_list=["ss.watch0.top"]))
