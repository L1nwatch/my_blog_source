#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 设置 articles 下的 url 对应的视图
"""
from django.conf.urls import url
import articles.views

__author__ = '__L1n__w@tch'

urlpatterns = [
    url(r"^$", articles.views.home, name="home"),
    url(r"^(\d+)/$", articles.views.detail, name="detail")
]

if __name__ == "__main__":
    pass
