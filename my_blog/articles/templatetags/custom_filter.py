#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 配置 markdown 等给模板使用的 filter
2017.02.11 需要给前端使用, 给特定关键字添加标签
2017.01.27 添加表格解析的支持, 添加 bleach 库用于清除不安全的 html 代码
"""
import markdown
import re
import html

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
    def replace(match_data):
        pre, raw_keyword = match_data.groups()
        pre = html.escape(pre)
        raw_keyword = "<em>{}</em>".format(raw_keyword)

        return "{}{}".format(pre, raw_keyword)

    def escape(match_data):
        pre, raw_keyword, suffix = match_data.groups()
        return "{}{}{}".format(pre, raw_keyword, html.escape(suffix))

    if "-" in raw_data:
        keyword, content = raw_data.split("-", 1)
        # 处理每个关键词的转义
        keyword_deal_re = re.compile("(?P<pre>[\s\S]*?)(?P<keyword>{})".format(keyword),
                                     flags=re.IGNORECASE)
        content = keyword_deal_re.sub(replace, content)

        # 专门处理一下最后一次匹配关键词后面的字符的转义
        suffix_escape_re = re.compile("(.*)(\<em\>{}\</em\>){{1}}(?P<suf>[\s\S]*)$".format(keyword),
                                      flags=re.IGNORECASE)
        content = suffix_escape_re.sub(escape, content)

        return mark_safe(content)
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
