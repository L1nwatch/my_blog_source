#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.02.09 把视图分离在两个 APP 的时候出现嵌套导入了, 所以只好弄一个 common 文件来存放了
"""
from ipware.ip import get_ip, get_real_ip, get_trusted_ip
from my_constant import const

import chardet
import copy
import logging
import os

__author__ = '__L1n__w@tch'

logger = logging.getLogger("my_blog.articles.views")


def create_search_result(article_list, keyword_set, search_type):
    """
    创建搜索结果以便返回给页面
    :param article_list: 存在关键词的文章列表
    :param keyword_set: set(), 每一个是一个用户搜索的关键词
    :param search_type: str(), 表示搜索结果的类型, 比如 "articles" or "journals"
    :return: list(), 每一个元素都是一个命名元组, 每一个元素的格式类似于: (id, title, content)
    """
    result_list = list()
    raw_keyword_set = copy.copy(keyword_set)

    for each_article in article_list:
        keyword_set = copy.copy(raw_keyword_set)

        result_content = str()
        # 遍历每一行, 提取出关键词所在行
        for each_line in each_article.content.splitlines():
            temp_keyword_set = set(copy.copy(keyword_set))

            # 已经搜索完所有关键词了, 就不浪费时间了
            if len(temp_keyword_set) <= 0:
                break

            for each_keyword in temp_keyword_set:
                if each_keyword.lower() in each_line.lower():
                    result_content += each_line + os.linesep
                    keyword_set.remove(each_keyword)
                    continue

        if len(result_content) <= 0:
            # 设置默认值
            result_content = const.KEYWORD_IN_TITLE

        result_list.append(const.ARTICLE_STRUCTURE(each_article.id, each_article.title, result_content, search_type))

    return result_list


def get_ip_from_django_request(request):
    """
    # 用来获取访问者 IP 的
    # 参考
    ## https://my.oschina.net/u/167994/blog/156184
    ## http://stackoverflow.com/questions/4581789/how-do-i-get-user-ip-address-in-django
    :param request: 传给视图函数的 request
    :return: ip 地址, 比如 116.26.110.36
    """
    logger.debug("获取 ip 情况, get_ip:{}, get_real_ip:{}, get_trusted_ip:{}"
                 .format(get_ip(request), get_real_ip(request), get_trusted_ip(request)))
    return get_ip(request)


def get_right_content_from_file(file_path):
    """
    读取文件时涉及到编码问题, 于是就专门写个函数来解决吧
    :param file_path: 文件路径
    :return: 文件内容, str() 形式
    """
    logging.debug("读取文件内容: {}".format(file_path))
    with open(file_path, "rb") as f:
        data = f.read()
        encoding = chardet.detect(data)["encoding"]

    try:
        data = data.decode("utf8")
    except UnicodeDecodeError:
        try:
            data = data.decode("gbk")
        except UnicodeDecodeError:
            data = data.decode(encoding)

    return data


if __name__ == "__main__":
    pass
