#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 对 toolhub 这个 APP 进行相关的视图测试

2017.03.24 编写有关视图首页的测试
"""
from django.test import TestCase
from toolhub.views import tools_name_list

__author__ = '__L1n__w@tch'


class HomeViewTest(TestCase):
    unique_url = "/tool_hub/"

    def test_use_right_template(self):
        """
        测试首页使用了正确的模板
        """
        response = self.client.get(self.unique_url)
        self.assertTemplateUsed(response, "toolhub_home.html")

    def test_display_all_tool_name(self):
        """
        首页应该显示所有工具的名字
        """
        response = self.client.get(self.unique_url)

        for each_tool_name in tools_name_list:
            self.assertContains(response, each_tool_name)


class GitHubPictureTranslateViewTest(TestCase):
    unique_url = "/tool_hub/github_picture_translate/"
    data_url = "/tool_hub/github_picture_translate/data"

    def test_use_right_template(self):
        response = self.client.get(self.unique_url)
        self.assertTemplateUsed(response, "github_picture_translate_tool/github_picture_translate_tool.html")

    def test_translate_right(self):
        response = self.client.get(self.data_url, {"raw_data": "2017-03-17首页截图.jpg"})
        right_answer = "2017-03-17%E9%A6%96%E9%A1%B5%E6%88%AA%E5%9B%BE.jpg"
        self.assertEqual(response.content.decode("utf8"), right_answer)


if __name__ == "__main__":
    pass
