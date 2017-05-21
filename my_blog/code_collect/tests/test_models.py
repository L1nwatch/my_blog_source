#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""  测试 code_collect 对应的 model

2017.05.21 修改 common_module 路径
2017.04.04 重构一下创建测试数据的代码
2017.03.28 新增 APP, 编写相关 model 测试
"""

from django.db.utils import IntegrityError

from code_collect.models import CodeCollect
from common_module.tests.basic_test import BasicTest

__author__ = '__L1n__w@tch'


class TestCodeCollect(BasicTest):
    def test_has_foreign_id_field(self):
        """
        测试该 model 应该有 note 字段, 用于链接 Article、GitBook 或者 Journal 的
        """
        # 提供了则不会报错
        self.create_code()

        # 不提供 note 信息, 则会报错
        with self.assertRaises(IntegrityError):
            CodeCollect.objects.create()

    def test_has_code_type_filed(self):
        """
        测试该 model 含有 code_type 字段, 用于表明某篇笔记含有的代码类型
        """
        note = self.create_article()

        # 提供了则不会报错
        self.create_code(note=note)

        # 不提供 code_type 信息, 则默认值为空
        cc = CodeCollect.objects.create(note=note)
        self.assertEqual(cc.code_type, "")

    def test_model_save_ignore_case(self):
        """
        测试该 model 保存的时候会无视大小写信息
        """
        code_type = "pytHOn"

        cc = self.create_code(code_type=code_type)

        self.assertEqual(cc.code_type, code_type.lower())


if __name__ == "__main__":
    pass
