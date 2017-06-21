#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 这里存放的是由于交叉引用导致无法编写在 common_help_function 的视图函数

2017.06.21 新增一个自定义的 404 页面
2017.06.17 新增一个映射 Tag 搜索的公共函数
"""

# 标准库
import logging
from django.http import Http404
from django.shortcuts import render

# 自己的模块
import my_constant as const

from articles.models import Tag
from common_module.common_help_function import model_dict, log_wrapper, get_context_data

__author__ = '__L1n__w@tch'

logger = logging.getLogger("my_blog.common_module.views")


@log_wrapper(str_format="进行了 Tag 搜索", logger=logger)
def search_tag_view(request, search_type, tag_name):
    """
    负责进行 tag 搜索, 可以区分是搜索 GitBook 还是搜索 Articles
    :param request: Django request 请求对象
    :param search_type: str(), 要搜索的类型, 比如 "articles"
    :param tag_name: str(), 要搜索的 Tag 名字
    :return: 渲染过后的搜索结果或者 404
    """
    if search_type not in model_dict:
        raise Http404
    if search_type not in ("articles", "gitbooks", "gitbook_notes"):
        # 默认是搜索 Article 笔记下的 Tag
        search_type = "articles"
    # 进行对应的搜索
    try:
        search_tag = Tag.objects.get(tag_name=tag_name)
        post_list = model_dict[search_type].objects.filter(tag=search_tag)
    except (model_dict[search_type].DoesNotExist, Tag.DoesNotExist):
        raise Http404

    return render(request, const.TAG_TEMPLATE, get_context_data(request, "articles", {'post_list': post_list}))


def handler404(request):
    response = render(request, 'common_404.html')
    response.status_code = 404
    return response


if __name__ == "__main__":
    pass
