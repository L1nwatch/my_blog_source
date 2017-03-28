#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""  测试 code_collect 对应的 model

2017.03.28 新增 APP, 编写相关 model 测试
"""
from django.test import TestCase
from django.db.utils import IntegrityError

from code_collect.models import CodeCollect
from articles.models import Article

__author__ = '__L1n__w@tch'


class TestCodeCollect(TestCase):
    def test_has_foreign_id_field(self):
        """
        测试该 model 应该有 note 字段, 用于链接 Article、GitBook 或者 Journal 的
        """
        code_type = "python"

        # 提供了则不会报错
        note = Article.objects.create(title="test", content="test")
        CodeCollect.objects.create(code_type=code_type, note=note)

        # 不提供 note 信息, 则会报错
        with self.assertRaises(IntegrityError):
            CodeCollect.objects.create(code_type=code_type)

    def test_has_code_type_filed(self):
        """
        测试该 model 含有 code_type 字段, 用于表明某篇笔记含有的代码类型
        """
        note = Article.objects.create(title="aaa", content="bbb")

        # 提供了则不会报错
        code_type = "python"
        CodeCollect.objects.create(code_type=code_type, note=note)

        # 不提供 code_type 信息, 则默认值为空
        cc = CodeCollect.objects.create(note=note)
        self.assertEqual(cc.code_type, "")

    def test_model_save_ignore_case(self):
        """
        测试该 model 保存的时候会无视大小写信息
        """
        note = Article.objects.create(title="test", content="test")
        code_type = "pytHOn"

        cc = CodeCollect.objects.create(note=note, code_type=code_type)

        self.assertEqual(cc.code_type, code_type.lower())


if __name__ == "__main__":
    pass
