#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.06.24 新增 sangfor 菜单测试, 将硬编码的 URL 改成常量
2017.05.15 新增有关转盘页面选择地点功能的相关测试
2017.03.22 新增有关转盘的相关测试
2017.02.05 测试视图函数
"""
# 标准库
from django.test import TestCase

# 自己的模块
from just_eating.views import school_lunch_backup_list, school_dinner_backup_list
import my_constant as const

__author__ = '__L1n__w@tch'


class TestHomeView(TestCase):
    unique_url = const.JUST_EATING_HOME_URL

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

    def test_href_to_each_place_eating(self):
        """
        测试首页有链接到各个地方吃饭计划表的按钮
        """
        for each_place in ("home", "school", "sangfor"):
            response = self.client.get(self.unique_url)
            self.assertContains(response, "{}{}".format(self.unique_url, each_place),
                                msg_prefix="[-] 缺少指向 {} 的链接".format(each_place))


class TestEatingView(TestCase):
    """
    测试 sangfor/school 的菜单显示
    """
    unique_urls = [const.JUST_EATING_SCHOOL_MENU_URL, const.JUST_EATING_SANGFOR_MENU_URL]

    def test_school_eating_template(self):
        for each_url in self.unique_urls:
            response = self.client.get(each_url)
            self.assertTemplateUsed(response, "just_eating_base.html",
                                    msg_prefix="[-] URL {} 没有使用指定模板".format(each_url))

    def test_display_school_eating_plan(self):
        """
        测试是否显示了 School/Sangfor 的吃饭计划
        """
        for each_url, each_title in zip(self.unique_urls, ["School", "Sangfor"]):
            response = self.client.get(each_url)
            self.assertContains(response, each_title, msg_prefix="[-] 缺少地点 {} 的吃饭计划".format(each_title))


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
