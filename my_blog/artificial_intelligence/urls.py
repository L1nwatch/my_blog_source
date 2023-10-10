#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 保存 app_life_summary 相关的 URL 映射

2023.09.23 新增入口
"""
# 标准库
from django.conf.urls import url

# 自己的模块
import artificial_intelligence.views

__author__ = '__L1n__w@tch'

urlpatterns = [
    url(r"^$", artificial_intelligence.views.update_file_and_send_email, name="ai_update_file"),
]
