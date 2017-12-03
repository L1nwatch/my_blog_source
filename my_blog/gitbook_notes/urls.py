#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
设置 app: gitbook_notes 对应的 url 映射

2016.10.30 准备开始把 gitbook 的代码放进博客中, 觉得新建一个 app 较好, 毕竟这个并不像文章一样展现出来
"""
from django.conf.urls import url
import gitbook_notes.views

__author__ = '__L1n__w@tch'

urlpatterns = [
    url(r"^update_gitbook_codes/$", gitbook_notes.views.update_gitbook_codes, name="update_gitbook_codes"),
    url(r"^(?P<gitbook_id>\d+)/$", gitbook_notes.views.gitbook_display, name="gitbook_display"),
]
