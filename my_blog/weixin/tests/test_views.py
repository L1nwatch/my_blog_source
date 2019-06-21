#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 测试微信公众号相关视图

2019.03.23 开始编写单测
"""
# 标准库
import unittest.mock

# 自己的模块
from common_module.tests.basic_test import BasicTest
import my_constant as const

__author__ = '__L1n__w@tch'


class WeiXinViewTest(BasicTest):
    unique_url = const.WEIXIN_URL

    def test_get_without_params(self):
        """
        没有任何传参的 get,报 404
        :return:
        """
        response = self.client.get(self.unique_url)
        self.assertTrue(response.status_code == 404)

    def test_get_with_wrong_params(self):
        """
        错误的验证, 也是报 404
        :return:
        """
        response = self.client.get(self.unique_url, data={"nonce": 1, "timestamp": 2, "echostr": 3, "signature": 4})
        self.assertTrue(response.status_code == 404)

    def test_get_with_right_params(self):
        """
        正确的验证,返回 echostr 串
        :return:
        """
        echo_str = '4970133915065778087'
        nonce = '68862302'
        timestamp = '1553308935'
        signature = 'c5db0bcbd7bb27834f6d80e0235eb7d630f1b6fb'

        response = self.client.get(self.unique_url, data={
            "nonce": nonce, "timestamp": timestamp, "echostr": echo_str, "signature": signature
        })
        self.assertTrue(response.status_code == 200)
        self.assertEqual(response.content, echo_str.encode("utf8"))

    def test_post_random_message(self):
        """
        测试 post 消息, 发啥会啥
        :return:
        """
        test_string = self.get_random_string(10)
        test_content = b'<xml><ToUserName><![CDATA[gh_a636453a97c2]]></ToUserName>\n<FromUserName><![CDATA[oqjYJ53uuUhJTGPtpy3CaexoQ7Sk]]></FromUserName>\n<CreateTime>1553309157</CreateTime>\n<MsgType><![CDATA[text]]></MsgType>\n<Content><![CDATA[' + test_string.encode(
            "utf8") + b'test]]></Content>\n<MsgId>22238041993306123</MsgId>\n</xml>'
        response = self.client.post(self.unique_url, data=test_content, content_type="text/xml")
        self.assertTrue(response.status_code == 200)
        self.assertIn(test_string.encode("utf8"), response.content)

    def test_post_stock_message(self):
        """
        测试 post 股票, 会调用股票函数
        :return:
        """
        test_string = "股票"
        test_content = b'<xml><ToUserName><![CDATA[gh_a636453a97c2]]></ToUserName>\n<FromUserName><![CDATA[oqjYJ53uuUhJTGPtpy3CaexoQ7Sk]]></FromUserName>\n<CreateTime>1553309157</CreateTime>\n<MsgType><![CDATA[text]]></MsgType>\n<Content><![CDATA[' + test_string.encode(
            "utf8") + b']]></Content>\n<MsgId>22238041993306123</MsgId>\n</xml>'

        with unittest.mock.patch("weixin.views.get_image_reply") as mock_get_stock_info:
            self.assertFalse(mock_get_stock_info.called)
            response = self.client.post(self.unique_url, data=test_content, content_type="text/xml")
            self.assertTrue(response.status_code == 200)
            self.assertTrue(mock_get_stock_info.called)
