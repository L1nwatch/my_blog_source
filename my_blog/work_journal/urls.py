#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.02.03 开始 APP 日常工作记录
"""
from django.conf.urls import url
import work_journal.views

__author__ = '__L1n__w@tch'

urlpatterns = [
    url(r"^$", work_journal.views.work_journal_home_view, name="work_journal"),
    url(r"^(?P<journal_id>\d+)/$", work_journal.views.journal_display, name="journal_display"),
]

if __name__ == "__main__":
    pass
