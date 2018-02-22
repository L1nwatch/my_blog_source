#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""

2017.10.14 新增凯撒加密的工具, 不过还没提供到前台
2017.06.15 新增一个 html 文件的判断函数
2017.06.14 新增一个有关静态 HTML 映射的视图函数
2017.05.21 修改 common_module 路径
2017.03.25 新增 form, 更改 ajax 为 post 请求
2017.03.24 新增 toolhub 这个 APP
"""
# 标准库
import logging
import os
from urllib.parse import quote

from django.http import HttpResponse, Http404
from django.shortcuts import render

# 自己的模块
from toolhub.cryptography.caesar_cipher import Caesar
from common_module.common_help_function import log_wrapper, is_static_file_exist
from toolhub.forms import GitHubTranslateTextareaForm, CaesarCipherTextareaForm

__author__ = '__L1n__w@tch'

logger = logging.getLogger("my_blog.gitbooks.views")

tools_name_list = ["GitHub 图片地址转换"]


@log_wrapper(str_format="使用了凯撒加密", level="info", logger=logger)
def view_caesar_cipher(request):
    form = CaesarCipherTextareaForm(auto_id=False)
    return render(request, "caesar_cipher/caesar_cipher.html",
                  {"textarea_form": form})


@log_wrapper(str_format="访问了 ToolHub 首页", level="info", logger=logger)
def toolhub_home_view(request):
    return render(request, "toolhub_home.html")


@log_wrapper(str_format="访问了 GitHub 图片地址转换工具", level="info", logger=logger)
def github_picture_translate_tool_view(request):
    form = GitHubTranslateTextareaForm(auto_id=False)
    return render(request, "github_picture_translate_tool/github_picture_translate_tool.html",
                  {"textarea_form": form})


@log_wrapper(str_format="使用了 GitHub 图片地址转换工具", level="info", logger=logger)
def github_picture_translate(request):
    if request.method == "POST":
        raw_data = request.POST["raw_data"]
        return HttpResponse(quote(raw_data))
    return HttpResponse("test")


@log_wrapper(str_format="凯撒解密工具", level="info", logger=logger)
def caesar_cipher_decrypt(request):
    if request.method == "POST":
        raw_data = request.POST["raw_data"]
        caesar = Caesar()
        return HttpResponse(caesar.decrypt(raw_data, 7))
    return HttpResponse("test")


@log_wrapper(str_format="凯撒加密工具", level="info", logger=logger)
def caesar_cipher_encrypt(request):
    if request.method == "POST":
        raw_data = request.POST["raw_data"]
        caesar = Caesar()
        return HttpResponse(caesar.encrypt(raw_data, 7))
    return HttpResponse("test")


@log_wrapper(str_format="访问了静态 HTML 文件", level="info", logger=logger)
def static_html_map(request, html_file_name):
    if not str(html_file_name).endswith(".html"):
        raise Http404("[-] Not HTML File")
    elif not is_static_file_exist(html_file_name):
        raise Http404("[-] You should not read this file!")
    return render(request, os.path.join("static_htmls", html_file_name))
