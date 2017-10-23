#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 配置 markdown 等给模板使用的 filter

2017.06.06 再次修正, 现在可以确保正常内容、内联代码、代码块中的 XSS 攻击都正常显示了
2017.06.05 bleach 是为了保证 md 文件无法输送恶意语句, 但是因此也会导致 code 的显示不正确, 现在进行修正
2017.05.24 并不了解当初为什么把 bleach 注释掉了, 现在补回来, 因为缺少这一句发现了 BUG
2017.02.26 添加一个菜单格式化器
2017.02.11 需要给前端使用, 给特定关键字添加标签
2017.01.27 添加表格解析的支持, 添加 bleach 库用于清除不安全的 html 代码
"""
import markdown
import re
import html
import bleach

# import markdown2
# from django.utils.encoding import force_text

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

__author__ = '__L1n__w@tch'

register = template.Library()  # 自定义filter时必须加上


def translate_keyword(keyword):
    """
    转义函数, 例如把 ( 转义成 \(, 防止编译正则失败
    :param keyword:
    :return:
    """
    string = r"""\()[]{}><"?'$%"""
    for each_str in string:
        keyword = keyword.replace(each_str, r"\{}".format(each_str))

    return keyword


@register.filter(is_safe=True)  # 注册template filter
@stringfilter  # 希望字符串作为参数
def add_em_tag(keyword, raw_content):
    def replace(match_data):
        pre, raw_keyword = match_data.groups()
        pre = html.escape(pre)
        raw_keyword = "<em>{}</em>".format(raw_keyword)

        return "{}{}".format(pre, raw_keyword)

    def escape(match_data):
        pre, raw_keyword, suffix = match_data.groups()
        return "{}{}{}".format(pre, raw_keyword, html.escape(suffix))

    if keyword != "":
        keyword = translate_keyword(keyword)

        # 处理每个关键词的转义
        keyword_deal_re = re.compile("(?P<pre>[\s\S]*?)(?P<keyword>{})".format(keyword),
                                     flags=re.IGNORECASE)
        content = keyword_deal_re.sub(replace, raw_content)

        # 专门处理一下最后一次匹配关键词后面的字符的转义
        suffix_escape_re = re.compile("(.*)(\<em\>{}\</em\>){{1}}(?P<suf>[\s\S]*)$".format(keyword),
                                      flags=re.IGNORECASE)
        content = suffix_escape_re.sub(escape, content)

        return mark_safe(content)
    else:
        return raw_content


@register.filter(is_safe=True)  # 注册template filter
@stringfilter  # 希望字符串作为参数
def custom_markdown(value):
    value = special_bleach_clean(value)  # 清除不安全因素

    result = markdown.markdown(value, extensions=["codehilite", "fenced_code", "tables", "toc"],
                               enable_attributes=False)

    return mark_safe(result)


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


def special_bleach_clean(raw_data):
    """
    按照自己的方式特殊进行 bleach.clean 操作, 主要是指不清除反引号以及代码块里的隐患
    :param raw_data: str(), 含有不安全的数据
    :return: str(), 按照特殊方式处理过后的数据
    """

    def __bleach_clean_pre(match_data):
        pre, raw_content = match_data.groups()

        return "{}{}".format(bleach.clean(pre), raw_content)

    def __bleach_clean_suf(match_data):
        pre, raw_content, suffix = match_data.groups()
        return "{}{}{}".format(pre, raw_content, bleach.clean(suffix))

    # 处理每个关键词的转义
    special_bleach_clean_re = re.compile("(?P<pre>[^`]*?)(?P<code>`[^`]*`)")
    result = special_bleach_clean_re.sub(__bleach_clean_pre, raw_data)

    # 专门处理一下最后一次匹配关键词后面的字符的转义
    # 这里的 {{1}} 表示把括号内的标记为组 1
    suffix_bleach_clean_re = re.compile("(.*)(`[^`]*`){1}(?P<suf>.*)$", flags=re.IGNORECASE)
    result = suffix_bleach_clean_re.sub(__bleach_clean_suf, result)

    return result


@register.filter(is_safe=True)
@stringfilter
def menu_format(raw_data):
    food_lists = raw_data.split("\n")
    href_re = re.compile("(.*)\?href=(.*)")
    result_list = list()

    for each_food in food_lists:
        if "?href=" in each_food:
            result = href_re.findall(each_food)[0]
            result_list.append('<a href="{}">{}</a>'.format(result[1], result[0]))
        elif each_food != "":
            result_list.append('<a href="#">{}</a>'.format(each_food))

    return mark_safe("<br/>".join(result_list))


def unescape_tag_in_code(html_content):
    """
    确保所有 code 标签内的 tag 都没有被转义
    :param html_content: str(), 比如 "<code>&amp;lt;script&amp;gt;</code><code>&amp;lt;script&amp;gt;</code>"
    :return: str(), 确保没有转义, 比如 "<code><script></code><code><script></code>"
    """

    def __unescape_in_code(data):
        content = data.group(1)

        return "<code>{}</code>".format(html.unescape(content))

    unescape_tag_in_code_re = re.compile("<code>(?P<content>.*?)</code>")

    result = unescape_tag_in_code_re.sub(__unescape_in_code, html_content)
    return result


if __name__ == "__main__":
    pass
