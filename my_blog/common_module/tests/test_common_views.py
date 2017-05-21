#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 进行共通的测试
很多测试得在 Article、Journal、GitBook 分别做, 所以干脆合在一起测试好了

2017.05.21 重构, 将通用的 view 测试放到这个文件里面
"""
# 自己写的代码模块导入
from .basic_test import BasicTest, search_url

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

            response = self.client.post(search_url, data={"search_content": "test", "search_choice": types})

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


if __name__ == "__main__":
    pass
