#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.05.15 新增有关转盘页面选择地点功能的相关测试
2017.03.22 新增有关转盘的相关测试
2017.02.05 测试视图函数
"""
from just_eating.views import school_lunch_backup_list, school_dinner_backup_list
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


class TestRandomEatingView(TestCase):
    unique_url = "/just_eating/random_eating/{}"

    def test_backup_list_display(self):
        """
        测试备选菜单中的每一项都显示在了界面中
        """
        # 学校午饭的菜单
        response = self.client.get(self.unique_url.format("school_lunch"))
        for each_backup_food in school_lunch_backup_list:
            self.assertContains(response, each_backup_food)

        # 学校晚饭的菜单
        response = self.client.get(self.unique_url.format("school_dinner"))
        for each_backup_food in school_dinner_backup_list:
            self.assertContains(response, each_backup_food)

    def test_use_spinner_template(self):
        response = self.client.get(self.unique_url.format("school_lunch"))
        self.assertTemplateUsed(response, "just_eating_spinner.html")

    def test_title_display(self):
        """
        测试标题会随着地点的不同而显示不同
        """
        label = '<button id="id_eating_what" class="dropbtn">{}</button>'

        # 学校午饭的菜单
        response = self.client.get(self.unique_url.format("school_lunch"))
        self.assertContains(response, label.format("学校午饭"))

        # 学校晚饭的菜单
        response = self.client.get(self.unique_url.format("school_dinner"))
        self.assertContains(response, label.format("学校晚饭"))


if __name__ == "__main__":
    pass
