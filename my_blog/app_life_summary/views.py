# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.06.30 新增 life_summary 视图函数
"""

# 标准库
from django.shortcuts import render

# 自己的模块
import my_constant as const


def life_summary(request):
    return render(request, const.LIFE_SUMMARY_TEMPLATE)
