#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""

2016.10.07 给搜索按钮添加 form
"""
from django import forms

from .models import Article

from my_constant import const

__author__ = '__L1n__w@tch'


class ArticleForm(forms.models.ModelForm):
    class Meta:
        model = Article
        fields = ("title",)  # 注意逗号不可省略, 因为要表示成元组
        widgets = {
            "title": forms.fields.TextInput(attrs={
                "id": "id_search",
                "placeholder": const.PLACE_HOLDER,
                "class": "pure-input-2-3",
            })
        }
        error_messages = {
            "title": {"required": const.EMPTY_ARTICLE_ERROR}
        }


if __name__ == "__main__":
    pass
