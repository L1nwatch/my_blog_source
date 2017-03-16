#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.03.16 为搜索框重构 form
2017.02.08 重定义一个基类, 作为 Journal 和 Article 的 Form
2016.10.07 给搜索按钮添加 form
"""
from django import forms
from .models import SearchModel
from my_constant import const

from django.forms.utils import flatatt
from django.utils.safestring import mark_safe
from django.utils.html import format_html

__author__ = '__L1n__w@tch'


class SelectWithTitles(forms.Select):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure the titles dict exists
        self.search_choice = {}

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)

        output = [format_html('<select{}>', flatatt(final_attrs))]
                  # '<span id="id_current_search_choice">{}</span>'.format(self.choices[0][1])]

        options = self.render_options([value])
        if options:
            output.append(options)

        output.append('</select>')
        return mark_safe('\n'.join(output))

    def render_option(self, selected_choices, option_value, option_label):
        each_choice = '<option id="id_search_choices" value="{value}">{display}</option>'
        return each_choice.format(value=option_value,
                                  display=option_value.capitalize())


class CustomChoiceField(forms.ChoiceField):
    widget = SelectWithTitles

    def __init__(self, choices=(), *args, **kwargs):
        choice_pairs = [(c[0], c[1]) for c in choices]
        super().__init__(choices=choice_pairs, *args, **kwargs)
        self.widget.search_choice = dict([(c[0], c[1]) for c in choices])


class BaseSearchForm(forms.models.ModelForm):
    search_choice = CustomChoiceField(required=True, choices=SearchModel.SEARCH_CHOICES, initial="all")

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
            {"class": "search_dropdown"}
        )


class ArticleForm(BaseSearchForm):
    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)

        self.fields["search_content"].widget.attrs.update({
            "class": "pure-input-2-3"
        })


if __name__ == "__main__":
    pass
