#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.03.25 新增 form, 更改 ajax 为 post 请求
2017.03.24 新增 toolhub 这个 APP
"""
import logging

from toolhub.forms import TextareaForm
from articles.common_help_function import log_wrapper

from django.shortcuts import render
from django.http import HttpResponse
from urllib.parse import quote

__author__ = '__L1n__w@tch'

logger = logging.getLogger("my_blog.gitbooks.views")

tools_name_list = ["GitHub 图片地址转换"]


@log_wrapper(str_format="访问了 ToolHub 首页", level="info", logger=logger)
def toolhub_home_view(request):
    return render(request, "toolhub_home.html")


@log_wrapper(str_format="访问了 GitHub 图片地址转换工具", level="info", logger=logger)
def github_picture_translate_tool_view(request):
    form = TextareaForm(auto_id=False)
    return render(request, "github_picture_translate_tool/github_picture_translate_tool.html",
                  {"textarea_form": form})


@log_wrapper(str_format="使用了 GitHub 图片地址转换工具", level="info", logger=logger)
def github_picture_translate(request):
    if request.method == "POST":
        raw_data = request.POST["raw_data"]
        return HttpResponse(quote(raw_data))
    return HttpResponse("test")
