#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 保存 app_life_summary 相关的 URL 映射

2017.06.30 新增 app_life_summary 首页 URL 映射
"""
# 标准库
from django.conf.urls import url

# 自己的模块
import app_life_summary.views

__author__ = '__L1n__w@tch'

urlpatterns = [
    url(r"^$", app_life_summary.views.life_summary, name="life_summary"),
]

if __name__ == "__main__":
    pass
