#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.03.30 对 log 添加没有 request 时的支持
2017.03.28 增加 Code 这个 APP 有关的代码实现
2017.03.26 新增有关搜索输入特殊字符的检查
2017.03.23 增加有关搜索结果按关键词出现次数排序的相关代码
2017.03.17 重构 form 之后判断 form valid 的小 bug 也被修复了
2017.03.16 发现 request.get 如果采用给定的 form 会导致默认的 choice 失效, 原因未知
2017.03.08 进行部分重构
2017.03.07 添加一个 clean form data 的方法, 因为不知道怎么嵌入 form。。。
2017.02.10 添加搜索时不搜索图片的设定
2017.02.09 把视图分离在两个 APP 的时候出现嵌套导入了, 所以只好弄一个 common 文件来存放了
"""
from ipware.ip import get_ip, get_real_ip, get_trusted_ip
from my_constant import const
from articles.forms import ArticleForm, BaseSearchForm
from articles.models import Article, BaseModel
from work_journal.models import Journal
from work_journal.forms import JournalForm
from gitbook_notes.models import GitBook
from code_collect.models import CodeCollect

import chardet
import copy
import logging
import string
import re
import datetime

__author__ = '__L1n__w@tch'

model_dict = {"articles": Article,
              "journals": Journal, "work_journal": Journal,
              "all": BaseModel,
              "gitbooks": GitBook, "gitbook_notes": GitBook,
              "code": CodeCollect}


def get_context_data(request, context_type, update_data=None):
    """
    定制基础的模版数据
    :param request: django 请求
    :param context_type: str(), 表示上下文的类型, 比如 "articles"
    :param update_data: dict(), 除了基础数据外, 需要额外发送给模板的数据
    :return: dict(), 发送给模板的全部数据
    """
    form_dict = {"articles": ArticleForm, "journals": JournalForm,
                 "all": BaseSearchForm, "gitbooks": BaseSearchForm, "code": BaseSearchForm}

    data_return_to_base_template = {"form": form_dict[context_type](initial={"search_choice": context_type}),
                                    "current_type": context_type,
                                    "is_valid_click": "True",
                                    "{}_numbers".format(context_type): len(model_dict[context_type].objects.all())}
    if request.method == "POST":
        data_return_to_base_template["form"] = form_dict[context_type](request.POST)

    if isinstance(update_data, dict):
        data_return_to_base_template.update(update_data)

    return data_return_to_base_template


def search_keyword_in_model(keyword_set, model, search_fields):
    """
    分离出搜索函数中的 model 搜索
    :param keyword_set:  set(), 待查找的关键词列表
    :param model: model(), Django 的 model 对象, 比如 GitBook, Journals 等
    :param search_fields: list(), 每个元素表示要搜索的字段, 比如 ["content", "title"]
    :return: set(), 搜索结果的集合
    """
    result_set = set()
    keyword_iterator = iter(keyword_set)

    # 对全部数据进行过滤
    first_keyword = next(keyword_iterator, None)
    for each_field in search_fields:
        if each_field == "content":
            filter_result = model.objects.filter(content__icontains=first_keyword)
        elif each_field == "title":
            filter_result = model.objects.filter(title__icontains=first_keyword)
        else:
            raise RuntimeError("[-] 不支持的查询字段")
        result_set.update(filter_result)

    # 对剩下的每个关键词进行处理, 处理的是由上面过滤剩下的数据
    keyword = next(keyword_iterator, None)
    while keyword:
        temp_result_set = set()
        # 对每篇笔记进行查找, 依次对每个字段进行查找
        each_key_word = keyword.lower()
        for each_article in result_set:
            for each_field in search_fields:
                field = getattr(each_article, each_field)
                if each_key_word in field.lower():
                    temp_result_set.add(each_article)

        result_set = temp_result_set
        keyword = next(keyword_iterator, None)

    return result_set


def data_check(raw_data):
    """
    检查一下 form 接收到的 data 是否合法
    :param raw_data: str(), 原始字符串
    :return: boolean(), True or False, 表示合法或不合法
    """
    if len(raw_data) == 1 and raw_data in string.printable:
        return False
    elif raw_data.strip(string.punctuation) == "":
        return False
    return True


def form_is_valid_and_ignore_exist_error(my_form):
    """
    判断 form 表单是否合法, 其中判断过程中不认为 "已存在" 是个错误
    2017.03.08 重构, 使得几个搜索函数都用这个来判断表单合法性
    2016.10.11 重定义验证函数, 不再使用简单的 form.is_valid, 原因是执行搜索的时候发现不能搜索跟已存在的文章一模一样的标题关键词
    :param my_form: form 实例, 比如 form = ArticleForm(data=request.POST)
    :return: boolean(), True 表示 form 合法
    """
    if not my_form.is_valid():
        print("[*] 发现错误: {}".format(my_form.errors))
        return False
    elif not data_check(clean_form_data(my_form.data["search_content"])):
        print("[*] 输入数据不合法")
        return False
    return True


def clean_form_data(data):
    """
    手动清理 form data
    :param data: str(), 比如 " aa"
    :return: str(), 清理后的结果, 比如 "aa"
    """
    return data.strip()


def sort_search_result(result_list, keyword_set):
    """
    对搜索结果进行排序
    :param result_list: list(), 每一个元素是一个 const.ARTICLE_STRUCTURE 的命名元组
    :param keyword_set: set(), 比如 {"test"}, 用户查询的关键词集合
    :return: list(), 排完序的结果, 每一个元素是一个 const.ARTICLE_STRUCTURE
    """

    def __sorted_function(x):
        total_count = 0

        for each_keyword in keyword_set:
            total_count += model_dict[x.type].objects.get(id=x.id).content.lower().count(each_keyword.lower())
        return total_count

    result_list = sorted(result_list, key=__sorted_function, reverse=True)
    return result_list


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
        for line_number, each_line in enumerate(each_article.content.splitlines()):
            temp_keyword_set = set(copy.copy(keyword_set))

            # 已经搜索完所有关键词了, 就不浪费时间了
            if len(temp_keyword_set) <= 0:
                break

            for each_keyword in temp_keyword_set:
                if each_keyword.lower() in each_line.lower():
                    # 如果是图片的话:
                    if picture_re.match(each_line):
                        result_content_list.append(
                            const.SEARCH_RESULT_INFO("", const.KEYWORD_IN_HREF, 0)
                        )
                    # 存在于正文:
                    else:
                        result_content_list.append(
                            const.SEARCH_RESULT_INFO(each_keyword, each_line, line_number + 1)
                        )
                    keyword_set.remove(each_keyword)
                    continue

        if len(result_content_list) <= 0:
            # 设置默认值
            result_content_list = [const.SEARCH_RESULT_INFO("", const.KEYWORD_IN_TITLE, 0)]

        result_list.append(
            const.ARTICLE_STRUCTURE(each_article.id, each_article.title, result_content_list, search_type))

    return sort_search_result(result_list, raw_keyword_set)


def get_ip_from_django_request(request):
    """
    # 用来获取访问者 IP 的
    # 参考
    ## https://my.oschina.net/u/167994/blog/156184
    ## http://stackoverflow.com/questions/4581789/how-do-i-get-user-ip-address-in-django
    :param request: 传给视图函数的 request
    :return: ip 地址, 比如 116.26.110.36
    """
    return get_ip(request)


def get_right_content_from_file(file_path):
    """
    读取文件时涉及到编码问题, 于是就专门写个函数来解决吧
    :param file_path: 文件路径
    :return: 文件内容, str() 形式
    """
    # print("[*] 读取文件内容: {}".format(file_path))
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


def decorator_with_args(decorator_to_enhance):
    """
    这个函数将被用来作为装饰器. 使得被它装饰的装饰器可以接收多个参数
    """

    def decorator_maker(*args, **kwargs):
        def decorator_wrapper(func):
            return decorator_to_enhance(func, *args, **kwargs)

        return decorator_wrapper

    return decorator_maker


@decorator_with_args
def log_wrapper(func, str_format="", level="info", logger=None):
    now = datetime.datetime.today()

    def wrapper(request=None, *func_args, **func_kwargs):
        if request is not None:
            logger_func = getattr(logger, level)
            if len(func_kwargs) > 0:
                logger_func(("[*] IP {} 于 {} " + str_format + ", 相关参数为: {}")
                            .format(get_ip_from_django_request(request), now, func_kwargs))
            else:
                logger_func(("[*] IP {} 于 {} " + str_format).format(get_ip_from_django_request(request), now))
        return func(request, *func_args, **func_kwargs)

    return wrapper


if __name__ == "__main__":
    pass
