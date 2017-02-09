#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.02.03 为这个 APP 新建 FORM 类
"""
from django import forms
from .models import Journal
from my_constant import const
from articles.forms import BaseSearchForm

__author__ = '__L1n__w@tch'


class JournalForm(BaseSearchForm):
    class Meta:
        model = Journal
        fields = ("title",)  # 注意逗号不可省略, 因为要表示成元组
        widgets = {
            "title": forms.fields.TextInput(attrs={
                "id": "id_search_work_journal",
                "placeholder": const.PLACE_HOLDER,
                "class": "pure-input-2-3",
            })
        }
        error_messages = {
            "title": {"required": const.EMPTY_ARTICLE_ERROR}
        }


if __name__ == "__main__":
    pass
