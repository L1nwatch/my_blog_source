#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 测试 homepage 这个 app 下的视图函数

2021-10-10 first unittest
"""
# 自己的模块
from common_module.tests.basic_test import BasicTest
import my_constant as const

__author__ = '__L1n__w@tch'


class TestHomePage(BasicTest):
    unique_url = const.HOMEPAGE_URL

    def test_homepage_use_right_template(self):
        response = self.client.get(self.unique_url)
        self.assertTemplateUsed(response, const.HOMEPAGE_TEMPLATE)

    def test_homepage_include_github_link(self):
        response = self.client.get(self.unique_url)
        self.assertContains(response, "github")
        self.assertContains(response, "https://github.com/L1nwatch")
        self.assertContains(response, "icon-social-github")

    def test_homepage_include_gitee_link(self):
        response = self.client.get(self.unique_url)
        self.assertContains(response, "gitee")
        self.assertContains(response, "https://gitee.com/w4tch")
        self.assertContains(response, "icon-social-github")

    def test_homepage_include_linkedin_link(self):
        response = self.client.get(self.unique_url)
        self.assertContains(response, "linkedin")
        self.assertContains(response, "https://www.linkedin.com/in/%E4%B8%B0-%E6%9E%97-ba4495102/")
        self.assertContains(response, "icon-social-linkedin")

    def test_homepage_include_we_chall_link(self):
        response = self.client.get(self.unique_url)
        self.assertContains(response, "WeChall")
        self.assertContains(response, "http://www.wechall.net/profile/WATCH")
        self.assertContains(response, "icon-game-controller")

    def test_homepage_include_jira_link(self):
        response = self.client.get(self.unique_url)
        self.assertContains(response, "jira")
        self.assertContains(response, "https://w4tch.atlassian.net/jira")
        self.assertContains(response, "icon-key")

    def test_homepage_include_confluence_link(self):
        response = self.client.get(self.unique_url)
        self.assertContains(response, "confluence")
        self.assertContains(response, "https://w4tch.atlassian.net/wiki")
        self.assertContains(response, "icon-docs")

    def test_homepage_include_mailto_link(self):
        response = self.client.get(self.unique_url)
        self.assertContains(response, "mailto:watch1602@gmail.com")

    def test_homepage_include_blog_link(self):
        response = self.client.get(self.unique_url)
        self.assertContains(response, "watch0.top/articles")
        self.assertContains(response, "icon-note")
