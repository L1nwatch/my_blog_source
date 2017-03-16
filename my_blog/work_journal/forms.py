#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.03.15 重构搜索的 form 和 model
2017.02.03 为这个 APP 新建 FORM 类
"""
from my_constant import const

from articles.forms import BaseSearchForm

__author__ = '__L1n__w@tch'


class JournalForm(BaseSearchForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["search_content"].widget.attrs.update({
            "class": "pure-input-2-3",
            "id": "id_search_work_journal"
        })


if __name__ == "__main__":
    pass
