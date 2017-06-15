#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" toolhub 的相关 url

2017.06.14 新增有关静态 HTML 映射的 URL
2017.03.24 开始新建 toolhub, 先存放一个 GitHub 图片地址转换器
"""
# 标准库
from django.conf.urls import url

# 自己的模块
import toolhub.views
import my_constant as const

__author__ = '__L1n__w@tch'

urlpatterns = [
    url(r"^$", toolhub.views.toolhub_home_view, name="toolhub_home"),
    url(r"^github_picture_translate/$", toolhub.views.github_picture_translate_tool_view,
        name="github_picture_translate"),
    url(r"^github_picture_translate/data$", toolhub.views.github_picture_translate),
    url(r"^html(?P<html_file_name>.*\.html)$".format(const.TOOLHUB_STATIC_HTML_URL),
        toolhub.views.static_html_map, name="static_html_map"),
]

if __name__ == "__main__":
    pass
