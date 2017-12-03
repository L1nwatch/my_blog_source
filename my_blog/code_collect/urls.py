#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 设置 code_collect 对应的 URL 映射

2017.03.29 新增一个 do_code_search URL 映射
2017.03.28 新增一个 code_collect URL, 用于更新对应数据库信息
"""
from django.conf.urls import url

import code_collect.views

__author__ = '__L1n__w@tch'

urlpatterns = [
    url(r"^code_collect/$", code_collect.views.code_collect),
    url(r"^do_code_search/$", code_collect.views.do_code_search),
]
