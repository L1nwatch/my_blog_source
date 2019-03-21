#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 保存 weixin 相关的 URL 映射

2019.03.21 新增 weixin 这个 APP,公众号使用
"""
# 标准库
from django.conf.urls import url

# 自己的模块
import weixin.views

__author__ = '__L1n__w@tch'

urlpatterns = [
    url(r"^$", weixin.views.check_signature, name="check_signature"),
]
