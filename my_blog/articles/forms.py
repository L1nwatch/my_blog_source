#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""

2016.10.07 给搜索按钮添加 form
"""
from django import forms

from .models import Article

__author__ = '__L1n__w@tch'

EMPTY_ARTICLE_ERROR = "没有相关文章题目"
PLACE_HOLDER = "title to search"


class ArticleForm(forms.models.ModelForm):
    class Meta:
        model = Article
        fields = ("title",)  # 注意逗号不可省略, 因为要表示成元组
        widgets = {
            "title": forms.fields.TextInput(attrs={
                "id": "id_search",
                "placeholder": PLACE_HOLDER,
                "class": "pure-input-3-3"
            })
        }
        error_messages = {
            "title": {"required": EMPTY_ARTICLE_ERROR}
        }


if __name__ == "__main__":
    pass
