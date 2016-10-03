#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2016.10.03 测试网站的 ico 图片是否能够正常读取
"""
from django.test import TestCase

__author__ = '__L1n__w@tch'


class TestGetICO(TestCase):
    def test_get_ico_success(self):
        response = self.client.get("/static/favicon.ico")
        response = self.client.get("/")
        print(response.content.decode("utf8"))
        self.assertTrue(response.status_code != 404)


if __name__ == "__main__":
    pass
