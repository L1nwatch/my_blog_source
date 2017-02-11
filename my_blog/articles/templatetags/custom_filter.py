#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 配置 markdown 等给模板使用的 filter
2017.02.11 需要给前端使用, 给特定关键字添加标签
2017.01.27 添加表格解析的支持, 添加 bleach 库用于清除不安全的 html 代码
"""
import markdown
# import bleach
import re

# import markdown2
# from django.utils.encoding import force_text

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

__author__ = '__L1n__w@tch'

register = template.Library()  # 自定义filter时必须加上


@register.filter(is_safe=True)  # 注册template filter
@stringfilter  # 希望字符串作为参数
def add_em_tag(raw_data):
    if "-" in raw_data:
        keyword, content = raw_data.split("-", 1)
        return mark_safe(
            re.sub("(?P<keyword>{})".format(keyword), "<em>\g<keyword></em>", content, flags=re.IGNORECASE))
    else:
        return raw_data


@register.filter(is_safe=True)  # 注册template filter
@stringfilter  # 希望字符串作为参数
def custom_markdown(value):
    # value = bleach.clean(value)  # 清除不安全因素

    return mark_safe(markdown.markdown(value,
                                       extensions=["codehilite", "fenced_code", "tables", "toc"],
                                       enable_attributes=False))


def custom_markdown_for_tree_parse(value):
    # value = bleach.clean(value)  # 清除不安全因素
    result = markdown.markdown(value,
                               extensions=["codehilite", "fenced_code", "tables", "toc"],
                               enable_attributes=False)
    result = remove_code_tag_in_h_tags(result)

    return mark_safe(result)


def remove_code_tag_in_h_tags(html_content):
    """
    把所有 <h>..</h> 标签中的 <code>..</code> 全部删除掉
    :param html_content: str(), 比如 "<h1>aaa<code>bbb</code></h1>"
    :return: str(), 删除后的结果, 比如 "<h1>aaa</h1>"
    """
    remove_code_tag = re.compile("<code>(?P<content>.*?)</code>")

    result, n = remove_code_tag.subn("\g<content>", html_content)
    while n > 0:
        result, n = remove_code_tag.subn("\g<content>", result)
    return result


# def custom_markdown(value):
#     return mark_safe(markdown2.markdown(force_text(value),
#                                         extras=["fenced-code-blocks", "cuddled-lists", "metadata", "tables",
#                                                 "spoiler"]))


if __name__ == "__main__":
    pass
