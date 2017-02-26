#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.02.05 测试视图函数
"""
from django.test import TestCase

__author__ = '__L1n__w@tch'


class TestHomeView(TestCase):
    unique_url = "/just_eating/"

    def setUp(self):
        super().setUp()

    def test_use_right_template(self):
        response = self.client.get(self.unique_url)
        self.assertTemplateUsed(response, "just_eating_base.html")

    def test_display_weekday(self):
        """
        测试是否显示了 周一/周二/周三/周四/周五/周六/周日
        """
        response = self.client.get(self.unique_url)
        for each_weekday in ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]:
            self.assertContains(response, each_weekday)

    def test_display_time_a_day(self):
        """
        测试是否显示了 早餐/午餐/晚餐
        """
        response = self.client.get(self.unique_url)
        for each_time in ["早餐", "午餐", "晚餐"]:
            self.assertContains(response, each_time)

    def test_display_as_a_table(self):
        """
        测试是否以表格的形式展现
        """
        response = self.client.get(self.unique_url)
        self.assertContains(response, "<table")
        self.assertContains(response, "</table>")

    def test_display_home_plan(self):
        """
        测试是否显示了家里的吃饭计划
        """
        response = self.client.get(self.unique_url)
        self.assertContains(response, "Home")
        self.assertNotContains(response, "School")

    def test_title_is_right(self):
        """
        测试网页中是否显示了标题
        """
        response = self.client.get(self.unique_url)
        self.assertContains(response, "<title>吃啥</title>")

    def test_href_to_school_eating(self):
        """
        首页应该有链接到学校吃饭计划表的按钮
        """
        response = self.client.get(self.unique_url)
        self.assertContains(response, "{}{}".format(self.unique_url, "home"))

    def test_href_to_home_eating(self):
        """
        首页应该有链接到在家吃饭计划表的按钮
        """
        response = self.client.get(self.unique_url)
        self.assertContains(response, "{}{}".format(self.unique_url, "home"))


class TestSchoolEatingView(TestCase):
    unique_url = "/just_eating/school"

    def test_school_eating_template(self):
        response = self.client.get(self.unique_url)
        self.assertTemplateUsed(response, "just_eating_base.html")

    def test_display_school_eating_plan(self):
        """
        测试是否显示了 School 的吃饭计划
        """
        response = self.client.get(self.unique_url)
        self.assertContains(response, "School")


if __name__ == "__main__":
    pass
