#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 设置 articles 下的 url 对应的视图
"""
from django.conf.urls import url
import articles.views

__author__ = '__L1n__w@tch'

urlpatterns = [
    url(r"^(?P<article_id>\d+)/$", articles.views.detail, name="detail"),
    url(r'^archives/$', articles.views.archives, name='archives'),
    url(r'^about_me/$', articles.views.about_me, name='about_me'),
    url(r'^tag(?P<tag>\w+)/$', articles.views.search_tag, name='search_tag'),
    url(r'^search/$', articles.views.blog_search, name='search_title'),
    url(r'^update_notes/$', articles.views.update_notes, name='update_notes'),
]

if __name__ == "__main__":
    pass
