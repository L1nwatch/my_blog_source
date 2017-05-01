#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 设置 articles 下的 url 对应的视图

2017.05.01 完善一下验证更新时间的前台交互代码, 使用 update_notes 下的 path 提供交互信息
"""
from django.conf.urls import url
import articles.views

__author__ = '__L1n__w@tch'

urlpatterns = [
    url(r"^(?P<article_id>\d+)/$", articles.views.article_display, name="detail"),
    url(r'^archives/$', articles.views.archives_view, name='archives'),
    url(r'^about_me/$', articles.views.about_me_view, name='about_me'),
    url(r'^tag(?P<tag>\w+)/$', articles.views.search_tag_view, name='search_tag'),
    url(r'^update_notes/$', articles.views.update_notes, name='update_notes'),
    url(r'^update_notes/data$', articles.views.update_note_check_view, name='update_notes_check'),
]

if __name__ == "__main__":
    pass
