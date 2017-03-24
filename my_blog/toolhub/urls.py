#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" toolhub 的相关 url

2017.03.24 开始新建 toolhub, 先存放一个 GitHub 图片地址转换器
"""
from django.conf.urls import url
import toolhub.views

__author__ = '__L1n__w@tch'

urlpatterns = [
    url(r"^$", toolhub.views.toolhub_home_view, name="toolhub_home"),
    url(r"^github_picture_translate/$", toolhub.views.github_picture_translate_tool_view,
        name="github_picture_translate"),
    url(r"^github_picture_translate/data$", toolhub.views.github_picture_translate),
]

if __name__ == "__main__":
    pass
