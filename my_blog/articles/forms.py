#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.02.08 重定义一个基类, 作为 Journal 和 Article 的 Form
2016.10.07 给搜索按钮添加 form
"""
from django import forms
from .models import Article, BaseModel
from my_constant import const

__author__ = '__L1n__w@tch'



class BaseSearchForm(forms.models.ModelForm):
    class Meta:
        model = BaseModel
        fields = ("title",)  # 注意逗号不可省略, 因为要表示成元组
        widgets = {
            "title": forms.fields.TextInput(attrs={
                "id": "id_search",
                "placeholder": const.PLACE_HOLDER,
            })
        }
        error_messages = {
            "title": {"required": const.EMPTY_ARTICLE_ERROR}
        }


class ArticleForm(BaseSearchForm):
    class Meta(BaseSearchForm.Meta):
        model = Article

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)

        self.fields["title"].widget.attrs.update({
            "class": "pure-input-2-3"
        })


if __name__ == "__main__":
    pass
