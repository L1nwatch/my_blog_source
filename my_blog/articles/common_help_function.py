#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.03.08 进行部分重构
2017.03.07 添加一个 clean form data 的方法, 因为不知道怎么嵌入 form。。。
2017.02.10 添加搜索时不搜索图片的设定
2017.02.09 把视图分离在两个 APP 的时候出现嵌套导入了, 所以只好弄一个 common 文件来存放了
"""
from ipware.ip import get_ip, get_real_ip, get_trusted_ip
from my_constant import const

import chardet
import copy
import logging
import re

__author__ = '__L1n__w@tch'

logger = logging.getLogger("my_blog.articles.views")


def search_keyword_in_model(keyword_set, model, search_fields=["content"]):
    """
    分离出搜索函数中的 model 搜索
    :param keyword_set:  set(), 待查找的关键词列表
    :param model: model(), Django 的 model 对象, 比如 GitBook, Journals 等
    :return: set(), 搜索结果的集合
    """
    result_set = set()

    # 对每个关键词进行处理
    for i, each_key_word in enumerate(keyword_set):
        # 获取上一次过滤剩下的文章列表, 如果是第一次则为全部文章
        if i == 0:
            for each_field in search_fields:
                if each_field == "content":
                    filter_result = model.objects.filter(content__icontains=each_key_word)
                elif each_field == "title":
                    filter_result = model.objects.filter(title__icontains=each_key_word)
                else:
                    raise RuntimeError("[-] 不支持的查询字段")
                result_set.update(filter_result)

        else:
            temp_result_set = set()
            # 对每篇文章进行查找, 先查找标题, 然后查找内容
            each_key_word = each_key_word.lower()
            for each_article in result_set:
                for each_field in search_fields:
                    field = getattr(each_article, each_field)
                    if each_key_word in field.lower():
                        temp_result_set.add(each_article)

            result_set = temp_result_set

    return result_set


def form_is_valid_and_ignore_exist_error(my_form):
    """
    判断 form 表单是否合法, 其中判断过程中不认为 "已存在" 是个错误
    2017.03.08 重构, 使得几个搜索函数都用这个来判断表单合法性
    2016.10.11 重定义验证函数, 不再使用简单的 form.is_valid, 原因是执行搜索的时候发现不能搜索跟已存在的文章一模一样的标题关键词
    :param my_form: form 实例, 比如 form = ArticleForm(data=request.POST)
    :return: boolean(), True 表示 form 合法
    """
    if my_form.is_valid() is True:
        return True
    elif len(my_form.errors) == 1 and re.search("具有.*的.*已存在", str(my_form.errors)):
        return True
    return False


def clean_form_data(data):
    """
    手动清理 form data
    :param data: str(), 比如 " aa"
    :return: str(), 清理后的结果, 比如 "aa"
    """
    return data.strip()


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
    picture_re = re.compile("!\[.*\]\(.*\)")

    for each_article in article_list:
        keyword_set = copy.copy(raw_keyword_set)

        result_content_list = list()
        # 遍历每一行, 提取出关键词所在行
        for each_line in each_article.content.splitlines():
            temp_keyword_set = set(copy.copy(keyword_set))

            # 已经搜索完所有关键词了, 就不浪费时间了
            if len(temp_keyword_set) <= 0:
                break

            for each_keyword in temp_keyword_set:
                if each_keyword.lower() in each_line.lower():
                    # 如果是图片的话:
                    if picture_re.match(each_line):
                        result_content_list.append(const.KEYWORD_IN_HREF)
                    # 存在于正文:
                    else:
                        result_content_list.append("{}-{}".format(each_keyword, each_line))
                    keyword_set.remove(each_keyword)
                    continue

        if len(result_content_list) <= 0:
            # 设置默认值
            result_content_list = [const.KEYWORD_IN_TITLE]

        result_list.append(
            const.ARTICLE_STRUCTURE(each_article.id, each_article.title, result_content_list, search_type))

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
