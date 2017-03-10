#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.03.10 重构一下添加 em 标签的函数
2017.02.26 添加关于菜单格式化的代码测试
2017.01.31 发现对自定义 markdown 解析方法有要求, 所以还是写个单元测试吧
"""
from django.test import TestCase
from my_constant import const
from articles.templatetags.custom_filter import remove_code_tag_in_h_tags, add_em_tag, menu_format

__author__ = '__L1n__w@tch'


class TestCustomMarkdown(TestCase):
    def test_remove_code_tag_in_h_tags(self):
        # 只有一个的情况
        test_data = "<h1>aaa<code>bbb</code></h1>"
        right_answer = "<h1>aaabbb</h1>"
        my_answer = remove_code_tag_in_h_tags(test_data)
        self.assertEqual(right_answer, my_answer)

        # 多个的情况
        test_data = "<h1>aaa<code>bbb</code></h1>\n<h2>aaa<code>bbb</code>ccc</h2>"
        right_answer = "<h1>aaabbb</h1>\n<h2>aaabbbccc</h2>"
        my_answer = remove_code_tag_in_h_tags(test_data)
        self.assertEqual(right_answer, my_answer)

        # 多个 code 的情况
        test_data = "<h1>aaa<code>bbb</code>ccc<code>ddd</code></h1>"
        right_answer = "<h1>aaabbbcccddd</h1>"
        my_answer = remove_code_tag_in_h_tags(test_data)
        self.assertEqual(right_answer, my_answer)


class TestCustomFilter(TestCase):
    def test_add_em_tag(self):
        """
        给前端用的, 对每个关键词添加 em 标签, 方便前端显示
        """
        test_data = "aaa", "user = aaa"
        right_answer = "user = <em>aaa</em>"
        my_answer = add_em_tag(*test_data)
        self.assertEqual(right_answer, my_answer)

        test_data = "aaa", "user = aAa"
        right_answer = "user = <em>aAa</em>"
        my_answer = add_em_tag(*test_data)
        self.assertEqual(right_answer, my_answer)

        test_data = "aaa", "user = aAa....aaA"
        right_answer = "user = <em>aAa</em>....<em>aaA</em>"
        my_answer = add_em_tag(*test_data)
        self.assertEqual(right_answer, my_answer)

        test_data = "", const.KEYWORD_IN_HREF
        right_answer = const.KEYWORD_IN_HREF
        my_answer = add_em_tag(*test_data)
        self.assertEqual(right_answer, my_answer)

        test_data = "as", "*   参考资料:[HTML `<table>` 标签的 align 属性](.asp"
        right_answer = "*   参考资料:[HTML `&lt;table&gt;` 标签的 align 属性](.<em>as</em>p"
        my_answer = add_em_tag(*test_data)
        self.assertEqual(right_answer, my_answer)

        test_data = 'gh', 'right_answer = "<h1>aaabbb</h1>"'
        right_answer = 'ri<em>gh</em>t_answer = &quot;&lt;h1&gt;aaabbb&lt;/h1&gt;&quot;'
        my_answer = add_em_tag(*test_data)
        self.assertEqual(right_answer, my_answer)

    def test_menu_format(self):
        """
        测试菜单格式化器, 可以自动按行添加 <br/> 标签还有超链接添加 a 标签等
        """
        # 情况1: 有换行符没 href 的
        test_data = "牛肉盖饭\n冬瓜汤"
        right_answer = ('<a href="#">牛肉盖饭</a>'
                        '<br/>'
                        '<a href="#">冬瓜汤</a>')
        my_answer = menu_format(test_data)
        self.assertEqual(right_answer, my_answer)

        # 情况2: 没换行符的
        test_data = "包菜肉片"
        right_answer = '<a href="#">包菜肉片</a>'
        my_answer = menu_format(test_data)
        self.assertEqual(right_answer, my_answer)

        # 情况3: 有 href 没换行符的
        test_data = "可乐鸡翅?href=http://www.xinshipu.com/zuofa/227911"
        right_answer = '<a href="http://www.xinshipu.com/zuofa/227911">可乐鸡翅</a>'
        my_answer = menu_format(test_data)
        self.assertEqual(right_answer, my_answer)

        # 情况4: 有 href 有换行符的
        test_data = ("可乐鸡翅?href=http://www.xinshipu.com/zuofa/227911\n"
                     "豆芽炒油豆腐?href=http://www.xinshipu.com/zuofa/116954")
        right_answer = ('<a href="http://www.xinshipu.com/zuofa/227911">可乐鸡翅</a>'
                        '<br/>'
                        '<a href="http://www.xinshipu.com/zuofa/116954">豆芽炒油豆腐</a>')
        my_answer = menu_format(test_data)
        self.assertEqual(right_answer, my_answer)

        # 情况5: 命名只有一个还带换行符的
        test_data = "可乐鸡翅\n"
        right_answer = '<a href="#">可乐鸡翅</a>'
        my_answer = menu_format(test_data)
        self.assertEqual(right_answer, my_answer)


if __name__ == "__main__":
    pass
