#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.03.17 设置所有页面都不显示 select_choice, 同时去掉多余的初始化显示
2017.03.16 为搜索框重构 form
2017.02.08 重定义一个基类, 作为 Journal 和 Article 的 Form
2016.10.07 给搜索按钮添加 form
"""
from django import forms
from .models import SearchModel
from my_constant import const

from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.utils.encoding import force_text

__author__ = '__L1n__w@tch'


class SelectWithTitles(forms.Select):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure the titles dict exists
        self.search_choice = {}

    def render_option(self, selected_choices, option_value, option_label):
        if option_value is None:
            option_value = ''
        option_value = force_text(option_value)
        if option_value in selected_choices:
            selected_html = mark_safe(' selected="selected"')
            if not self.allow_multiple_selected:
                # Only allow for a single selection.
                selected_choices.remove(option_value)
        else:
            selected_html = ''

        each_choice = '<option id="id_search_choices_{value}" value="{value}"{selected_html}>{display}</option>'
        return format_html(each_choice, value=option_value,
                           selected_html=selected_html,
                           display=option_value.capitalize())


class CustomChoiceField(forms.ChoiceField):
    widget = SelectWithTitles

    def __init__(self, choices=(), *args, **kwargs):
        choice_pairs = [(c[0], c[1]) for c in choices]
        super().__init__(choices=choice_pairs, *args, **kwargs)
        self.widget.search_choice = dict([(c[0], c[1]) for c in choices])


class BaseSearchForm(forms.models.ModelForm):
    search_choice = CustomChoiceField(required=True, choices=SearchModel.SEARCH_CHOICES,
                                      initial={"search_choice": "all"})

    class Meta:
        model = SearchModel
        fields = ("search_content", "search_choice")  # 注意逗号不可省略, 因为要表示成元组
        widgets = {
            "search_content": forms.fields.TextInput(attrs={
                "id": "id_search",
                "placeholder": const.PLACE_HOLDER,
            })
        }

        error_messages = {
            "search_content": {"required": const.EMPTY_ARTICLE_ERROR}
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['search_choice'].widget.attrs.update(
            {"class": "id_search_choice_select", "style": "display:none"}

        )


class ArticleForm(BaseSearchForm):
    # search_choice = CustomChoiceField(required=True, choices=SearchModel.SEARCH_CHOICES,
    #                                   initial={"search_choice": "articles"})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["search_content"].widget.attrs.update({
            "class": "pure-input-2-3"
        })

        # self.initial['search_choice'] = 'articles'


if __name__ == "__main__":
    pass
