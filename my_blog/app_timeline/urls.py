#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 给 timeline app 设置 url 用的

2017.06.29 新增 timeline 首页的 url
"""
# 标准库
from django.conf.urls import url

# 自己的模块
import app_timeline.views

__author__ = '__L1n__w@tch'

urlpatterns = [
    url(r"^$", app_timeline.views.travel_event_timeline, name="travel_event_timeline"),
]

if __name__ == "__main__":
    pass