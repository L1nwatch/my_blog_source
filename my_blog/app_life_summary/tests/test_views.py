#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 负责测试 life_summary 这个 APP 下的视图函数

2017.07.02 重构视图, 不硬编码 HTML 而是自动生成
2017.06.30 新增有关 life_summary 首页的视图测试
"""
# 标准库
from common_module.tests.basic_test import BasicTest

# 自己的模块
import my_constant as const

__author__ = '__L1n__w@tch'


class TestLifeSummary(BasicTest):
    unique_url = const.LIFE_SUMMARY_URL

    def test_life_summary_use_right_template(self):
        response = self.client.get(self.unique_url)
        self.assertTemplateUsed(response, const.LIFE_SUMMARY_TEMPLATE)

    def test_life_summary_display_right_information(self):
        response = self.client.get(self.unique_url)
        self.assertContains(response, "洗漱用品")
        self.assertContains(response, "生活习惯")

    def test_create_sidebar_right(self):
        """
        测试能够正确地创建页面左边的菜单栏
        """
        response = self.client.get(self.unique_url)

        test_ids = const.LIFE_SUMMARY_SIDEBAR_IDS
        test_names = const.LIFE_SUMMARY_SIDEBAR_NAMES

        for right_id, right_number, right_name in zip(test_ids, range(7), test_names):
            self.assertContains(response, '<li id="{}">'.format(right_id))
            self.assertContains(response, '<div>{}</div>'.format(right_number))
            self.assertContains(response, '<div>{}</div>'.format(right_name))

    def test_create_summary_right_in_style_1(self):
        """
        测试能够正确地创建页面的总结笔记(风格 1), 即类似于下面的情况
    <h1>洗漱用品</h1>
    <p>洗发水</p>
    <ul>
        <li>清扬，薄荷味，洗完确实没头屑，但是有油</li>
        <li>沙宣，黑色，千万不要买；红色那款想试就试吧</li>
        <li>xxx</li>
    </ul>
        """
        response = self.client.get(self.unique_url)

        # 正常情况
        self.assertContains(response, '<h1>洗漱用品</h1>')

        self.fail("还没写完")

    def test_create_summary_right_in_style_2(self):
        """
        测试能够正确地创建页面的总结笔记(风格 2), 即类似于下面的情况
    <h1>服装</h1>
    <p>衣服</p>
    <p>洗衣服</p>
    <ul>
        <li>洗衣袋
            <ul>
                <li>只用来洗袜子和内裤</li>
                <li>买大一点的洗衣袋</li>
            </ul>
        </li>
    </ul>
        """
        response = self.client.get(self.unique_url)

        # 正常情况

        self.fail("还没写完")

    def test_create_summary_right_in_style_3(self):
        """
        测试能够正确地创建页面的总结笔记(风格 3), 即类似于下面的情况
    <h1>服装</h1>
    <p>衣服</p>
    <ul>
        <li>裤子 3 条不够用，起码 4 条</li>
        <li style="list-style-type:none">
            <ul>
                <li>短裤可以去迪卡侬买拉链短裤</li>
                <li>反光运动服迪卡侬有</li>
                <li>裤子买跟亚马逊那条一样的材料，不会乱叫</li>
            </ul>
        </li>
    </ul>
        """
        response = self.client.get(self.unique_url)

        # 正常情况
        self.assertContains(response, '<h1>洗漱用品</h1>')
        self.assertContains(response, '<h1>洗漱用品</h1>')

        self.fail("还没写完")


if __name__ == "__main__":
    pass
