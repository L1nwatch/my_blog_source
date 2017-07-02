# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.07.02 重构一下视图, 现在菜单栏是由代码生成的而不是硬编码的了
2017.06.30 新增 life_summary 视图函数
"""

# 标准库
from django.shortcuts import render

# 自己的模块
import my_constant as const


def create_sidebar_items():
    """
    为左边的菜单栏创建 items
    """
    items = list()

    for each_id, each_number, each_name in zip(const.LIFE_SUMMARY_SIDEBAR_IDS, range(7),
                                               const.LIFE_SUMMARY_SIDEBAR_NAMES):
        items.append(const.LIFE_SUMMARY_SIDEBAR_ITEMS(each_id, each_number, each_name))

    return items


def life_summary(request):
    items = create_sidebar_items()
    return render(request, const.LIFE_SUMMARY_TEMPLATE, context={"post_items": items})
