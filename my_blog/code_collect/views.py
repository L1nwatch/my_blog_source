# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.03.28 新增一个 code_collect 视图函数, 用于更新数据库信息
"""
from django.shortcuts import redirect


def code_collect(request=None):
    return redirect("home")
