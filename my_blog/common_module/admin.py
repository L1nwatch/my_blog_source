#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 通用模块的管理设置

2017.05.25 为 IP 表添加相关管理接口
"""

__author__ = '__L1n__w@tch'

from django.contrib import admin
from .models import VisitedIP


# Register your models here.
class VisitedIPAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'times',)
    search_fields = ('ip_address', 'times',)
    list_filter = ("times",)


admin.site.register(VisitedIP, VisitedIPAdmin)

