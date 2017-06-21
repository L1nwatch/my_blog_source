#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 进行共通的测试
很多测试得在 Article、Journal、GitBook 分别做, 所以干脆合在一起测试好了

2017.06.21 新增自定义 404 页面的测试
2017.06.17 添加有关 GitBook、Articles Tag 搜索的测试
2017.05.21 重构, 将通用的 view 测试放到这个文件里面
"""
# 标准库
from django.test import override_settings
import requests

# 自己写的代码模块导入
from .basic_test import BasicTest
from articles.models import Tag
import my_constant as const
from common_module.common_help_function import model_dict

__author__ = '__L1n__w@tch'


class TestSearch(BasicTest):
    """
    测试与搜索相关的视图
    """

    def test_search_result_are_sorted(self):
        """
        搜索的结果应该是排序过后的, 排序结果依赖于 clicked 字段
        """
        for types in ("articles", "journals", "gitbooks"):
            create_func = self.create_func_map(types)
            # 创建 3 篇文章, 均包含关键词 test, 但是出现次数不一致
            test_note1 = create_func(content="test + test + test", click_times=0)
            test_note2 = create_func(content="test", click_times=3)
            test_note3 = create_func(content="test + test", click_times=1)

            response = self.client.post(const.SEARCH_URL, data={"search_content": "test", "search_choice": types})

            response_text = response.content.decode("utf8")
            note1_index = response_text.index(test_note1.title)
            note2_index = response_text.index(test_note2.title)
            note3_index = response_text.index(test_note3.title)

            self.assertTrue(note2_index < note3_index < note1_index)

    def test_url_visit_will_not_increase_click_times(self):
        """
        测试搜索结果通过 GET 请求访问 URL 不会增加 click_times 字段, 通过 POST 访问则会增加
        """
        for types in ("articles", "journals", "gitbooks"):
            create_func = self.create_func_map(types)
            model = self.model_map(types)
            display_url = self.display_url_map(types)

            test_note = create_func(click_times=0)
            for i in range(10):
                self.client.get(display_url.format(test_note.id))

            test_note = model.objects.get(id=test_note.id)
            self.assertTrue(test_note.click_times == 0)

            for i in range(10):
                self.client.post(display_url.format(test_note.id), data={"visited": True})
            test_note = model.objects.get(id=test_note.id)
            self.assertTrue(test_note.click_times == 10)

    def test_tag_search(self):
        """
        测试能够正常进行 Tag 搜索
        """
        # 确保存在对应的测试数据
        test_tag_name = "test"
        test_tag = [Tag.objects.create(tag_name=test_tag_name)]
        article, article2 = self.create_article(article_tag=test_tag), self.create_article(article_tag=test_tag)
        gitbook = self.create_gitbook(gitbook_tag=test_tag)

        test_search_type = ["articles", "gitbooks"]
        for each_search_type in test_search_type:
            response = self.client.get(const.TAG_SEARCH_URL.format(each_search_type, test_tag_name))

            model = model_dict[each_search_type]

            for each_note in model.objects.filter(tag=test_tag[0]):
                self.assertContains(response, each_note.title, msg_prefix="[-] {} 下存在未找到的笔记".format(each_search_type))


@override_settings(DEBUG=False)
class TestErrorPages(BasicTest):
    """
    测试比如 404、400 等页面的情况
    """

    def test_custom_404_pages(self):
        """
        Y 的任务是测试当访问不存在的 URL 时会跳转到 404 页面中
        """

        # Y 知道某个 url 不存在, 于是 Y 访问了该 URL
        response = self.client.get("/aaa")
        # Y 发现服务返回了 404 码
        self.assertTrue(response.status_code == 404)
        # 而且该 404 页面用的是自定义的模板页面
        self.assertTemplateUsed(response, "common_404.html")

        # Y 在想是不是所有页面访问都会得到 404, 于是它试着访问了一下首页
        response = self.client.get("/")
        # 发现首页并不是返回 404, 说明这是在访问不存在页面时才会返回 404 码
        self.assertFalse(response.status_code == 404)


if __name__ == "__main__":
    pass
