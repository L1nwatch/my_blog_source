#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 配置 markdown

2017.01.27 添加表格解析的支持, 添加 bleach 库用于清除不安全的 html 代码
"""
import markdown
import bleach
# import markdown2

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe

__author__ = '__L1n__w@tch'

register = template.Library()  # 自定义filter时必须加上


@register.filter(is_safe=True)  # 注册template filter
@stringfilter  # 希望字符串作为参数
def custom_markdown(value):
    value = bleach.clean(value)  # 清除不安全因素

    return mark_safe(markdown.markdown(value,
                                       extensions=["codehilite", "fenced_code", "tables"],
                                       enable_attributes=False))


# def custom_markdown(value):
#     return mark_safe(markdown2.markdown(force_text(value),
#                                         extras=["fenced-code-blocks", "cuddled-lists", "metadata", "tables",
#                                                 "spoiler"]))


if __name__ == "__main__":
    pass
