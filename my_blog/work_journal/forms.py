#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.03.17 去掉多余的初始化操作
2017.03.16 重构了 form 需要覆盖 search_choice 选项
2017.03.15 重构搜索的 form 和 model
2017.02.03 为这个 APP 新建 FORM 类
"""
from articles.forms import BaseSearchForm

__author__ = '__L1n__w@tch'


class JournalForm(BaseSearchForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["search_content"].widget.attrs.update({
            "class": "pure-input-2-3",
            "id": "id_search_work_journal"
        })

        # self.initial['search_choice'] = 'journals'
