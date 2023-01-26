#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 测试 homepage 这个 app 下的视图函数

2023-01-22 update homepage: https://github.com/L1nwatch/my_blog_source/issues/27
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
        self.assertContains(response, "icon-loop")

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

    def test_homepage_include_fei_su_link(self):
        response = self.client.get(self.unique_url)
        self.assertContains(response, "FeiSu")
        self.assertContains(response, "https://drxsfuqrht.feishu.cn/sheets/shtcnWVRIvNaaRjrECipxsPLP0c")
        self.assertContains(response, "icon-grid")

    def test_homepage_include_google_docs_link(self):
        response = self.client.get(self.unique_url)
        self.assertContains(response, "GgDocs")
        self.assertContains(response, "https://docs.google.com/spreadsheets/u/0/")
        self.assertContains(response, "icon-grid")

    def test_homepage_include_cv_and_resume(self):
        response = self.client.get(self.unique_url)
        self.assertContains(response, "Resume")
        self.assertContains(response, "http://watch0.top/resume")
        self.assertContains(response, "CV")
        self.assertContains(response, "http://watch0.top/cv")

        self.assertContains(response, "icon-grid")

    def test_homepage_has_4_types_link(self):
        response = self.client.get(self.unique_url)
        self.assertContains(response, "Social Media")  # Social Media(Resume/CV/LinkedIn/QQ/Wechat/GitHub Profile/...)
        self.assertContains(response, "Useful Platform")  # Useful Platform(Jira/Wiki/Notion/....)
        self.assertContains(response, "My Tool")  # My Tool(Articles/Menu/....)
        self.assertContains(response, "Fun Stuff")  # Fun Stuff

    def test_homepage_has_my_tools_from_ole_homepage(self):
        response = self.client.get(self.unique_url)
        self.assertContains(response, "Eating")
        self.assertContains(response, "Journal")
        self.assertContains(response, "Archives")
        self.assertContains(response, "ToolHub")
        self.assertContains(response, "Timeline")
        self.assertContains(response, "LifeSummary")
        self.assertContains(response, "GitBook")

    def test_homepage_fulfill_all_Places(self):
        response = self.client.get(self.unique_url)
        self.assertContains(response, "https://codepen.io/")
        self.assertContains(response, "https://to-do.live.com/tasks/today")
        self.assertContains(response, "https://www.olevod.com/")
        self.assertContains(response, "https://my.vultr.com/")
        self.assertContains(response, "https://ping.chinaz.com/")
        self.assertContains(response, "https://www.west.cn/")
        self.assertContains(response, "https://www.lastpass.com/")
        self.assertContains(response, "http://feijisu.icu/")
        self.assertContains(response, "https://photos.google.com/")
        self.assertContains(response, "https://stackoverflow.com/")
        self.assertContains(response, "https://music.youtube.com/")
        self.assertContains(response, "https://www.zhihu.com/column/testcircle")
