#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 负责测试 life_summary 这个 APP 下的视图函数

2017.07.09 继续补充完善 summary 解析树的测试
2017.07.02 重构视图, 不硬编码 HTML 而是自动生成
2017.06.30 新增有关 life_summary 首页的视图测试
"""
# 标准库
from common_module.tests.basic_test import BasicTest
from bs4 import BeautifulSoup, Tag

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

    @staticmethod
    def find_next_tag(tag):
        """
        在 bs4 解析树中查找某一个节点的下一个 Tag
        比如:
            <p>xxx</p>
            <ul>xxx</ul>
        则调用该函数找 p 的下一个 Tag 就是 ul
        :param tag: 某 tag
        :return: 该 tag 的下一个 Tag
        """
        for next_tag in tag.next_elements:
            if isinstance(next_tag, Tag):
                return next_tag

    def _summary_style_1(self, ul_root):
        """
        测试能够正确地创建页面的总结笔记(风格 1), 即类似于下面的情况
    <ul>
        <li>清扬，薄荷味，洗完确实没头屑，但是有油</li>
        <li>沙宣，黑色，千万不要买；红色那款想试就试吧</li>
        <li>xxx</li>
    </ul>
        :param ul_root: 包裹以上风格的 ul 父节点
        :return: True or False, 表示这里面是否存在这种风格
        """
        result = False

        try:
            # ul 节点应该没有 style
            assert not ul_root.has_attr("style")

            # ul 下面应该是 li 节点
            next_tag = self.find_next_tag(ul_root)
            assert next_tag.name == "li"

            # 每个 li 节点都没有 style 属性, 且每个 li 下无其他 Tag
            for each_li in ul_root.find_all("li"):
                assert not each_li.has_attr("style")
                for each_child in each_li.children:
                    assert not isinstance(each_child, Tag)

            result = True
        except AssertionError:
            pass

        return result

    def _summary_style_2(self, ul_root):
        """
        测试能够正确地创建页面的总结笔记(风格 2), 即类似于下面的情况
    <ul>
        <li>洗衣袋
            <ul>
                <li>只用来洗袜子和内裤</li>
                <li>买大一点的洗衣袋</li>
            </ul>
        </li>
    </ul>
        :param ul_root: 包裹以上风格的 ul 父节点
        :return: True or False, 表示这里面是否存在这种风格
        """
        result = False

        try:
            # ul 节点应该没有 style
            assert not ul_root.has_attr("style")

            # ul 下面应该是 li 节点
            next_tag = self.find_next_tag(ul_root)
            assert next_tag.name == "li"

            # 每一个 li 节点都没有 style, 且有对应 text
            lis = ul_root.find_all("li")
            for each_li in lis:
                assert not each_li.has_attr("style")
                assert each_li.text != ""

            # 其中一个 li 节点下面含有 ul 节点
            assert any(
                [self.find_next_tag(x).name == "ul" for x in lis]
            )

            result = True
        except AssertionError:
            pass

        return result

    def _summary_style_3(self, ul_root):
        """
        测试能够正确地创建页面的总结笔记(风格 3), 即类似于下面的情况
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
        :param ul_root: 包裹以上风格的 ul 父节点
        :return: True or False, 表示这里面是否存在这种风格
        """
        result = False

        try:
            # ul 节点应该没有 style
            assert not ul_root.has_attr("style")

            # ul 下面应该是 li 节点
            next_tag = self.find_next_tag(ul_root)
            assert next_tag.name == "li"

            # 至少有一个 li 节点存在 style
            style_li = ul_root.find("li", {"style": "list-style-type:none"})
            assert style_li

            # li 节点下面又是 ul 节点
            next_tag = self.find_next_tag(style_li)
            assert next_tag.name == "ul"

            result = True
        except AssertionError:
            pass

        return result

    def test_create_summary_right_in_styles(self):
        """
        测试每个 div 中的 html 树符合格式要求
        """
        response = self.client.get(self.unique_url)

        html_parse = BeautifulSoup(response.content)
        divs = html_parse.find_all("div", {"class": "desktop"})
        self.assertTrue(len(divs) > 0)  # 至少有一份总结

        for each_div in divs:
            # 应该有且只有一个 h1
            h1s = each_div.find_all("h1")
            self.assertTrue(len(h1s) == 1)

            # 有至少一个 p
            ps = each_div.find_all("p")
            self.assertTrue(len(ps) > 0)

            # 每个 p 下面是 ul
            for each_p in ps:
                # p 接下来是一个 ul 节点
                next_tag = self.find_next_tag(each_p)
                self.assertEqual(next_tag.name, "ul")

                # 每个 ul 里面的风格是指定 3 种风格之一
                self.assertTrue(any(
                    [x for x in [self._summary_style_1(next_tag),
                                 self._summary_style_2(next_tag),
                                 self._summary_style_3(next_tag)]]
                ), msg="[-] {} 不符合风格要求".format(next_tag))


if __name__ == "__main__":
    pass
