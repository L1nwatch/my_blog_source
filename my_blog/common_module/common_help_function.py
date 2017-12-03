#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""

2017.12.03 新增一个域名解析操作
2017.11.27 添加了硬编码 IP 还是没用,需要日志定位一下原因了, 好吧, 原来是硬编码错地方了
2017.11.26 硬编码允许访问的 IP
2017.08.26 新增一个 ip 限制的装饰器, 但是好像函数没什么用
2017.06.15 添加一个验证 html 文件存在的函数
2017.06.14 完善邮件发送的消息格式
2017.06.11 修复一下日志记录 deepcopy 导致的问题
2017.06.10 添加记录日志时获取指定的 HTTP 头信息 + 解决 request.META.items() 在遍历时会被修改的问题
2017.06.04 重构搜索结果数据结构 + 新增一个解析 tag 的函数
2017.06.03 修正笔记数的获取方式, 换了一个好像更高效的方法来统计
2017.06.03 继续重写代码逻辑, 避免数据库锁定以及发邮件卡顿的问题
2017.06.02 添加多线程, 主要是为了那个访问淘宝 IP 库的函数使用的
2017.06.02 优化排序代码 + 新增更新笔记数的功能
2017.05.25 在日志记录函数中新增发送邮件的操作
2017.05.21 修改 common_module 路径
2017.04.30 新增一个 is_valid_git_address 判断函数
2017.04.29 修改 log_wrapper, 强制使用关键字参数 + 完善元信息
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
# 自己的模块
import my_constant as const
from articles.forms import ArticleForm, BaseSearchForm
from articles.models import Article, BaseModel
from work_journal.models import Journal
from work_journal.forms import JournalForm
from gitbook_notes.models import GitBook
from code_collect.models import CodeCollect
from common_module.email_send import email_sender
from common_module.ip_deal import locate_using_ip_address, get_ip_from_django_request
from django.http import HttpResponse

# 标准库
import ipaddress
import socket
import logging
import chardet
import string
import re
import threading
import bleach
import datetime
import os
import copy

from functools import wraps

logger = logging.getLogger("my_blog.common_module.views")

__author__ = '__L1n__w@tch'

# 字符串与 Model 映射关系
model_dict = {"articles": Article,
              "journals": Journal, "work_journal": Journal,
              "all": BaseModel,
              "gitbooks": GitBook, "gitbook_notes": GitBook,
              "code": CodeCollect}


def is_valid_git_address(raw_data):
    return re.match("^https?://.+\.git$", raw_data)


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
                                    "{}_numbers".format(context_type): model_dict[context_type].objects.all().count()}
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


def sort_search_result(result_list):
    """
    对搜索结果进行排序, 按照点击次数来排序
    :param result_list: list(), 每一个元素是一个 const.ARTICLE_STRUCTURE 的命名元组
    :return: list(), 排完序的结果, 每一个元素是一个 const.ARTICLE_STRUCTURE
    """

    def __sorted_function(x):
        return x.note.click_times

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

        result_list.append(const.ARTICLE_STRUCTURE(
            each_article, result_content_list, search_type)
        )

    return sort_search_result(result_list)


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


def get_http_header_from_request(request):
    """
    从 django request 中获取对应的 http 头部信息
    :param request: django request 对象
    :return: dict(), 为 http 头部信息
    """
    result = list()
    http_headers = copy.copy(request.META)
    for each_key, each_value in http_headers.items():
        if each_key in const.LOG_HTTP_HEADERS_WHITE_LIST:
            result.append("{} -> {}".format(bleach.clean(each_key), bleach.clean(each_value)))

    return "\n".join(result)


def background_deal(*, logger, level, request, func_kwargs, str_format, ip_address, email_check):
    """
    记录日志 + 发送邮件
    :param ip_address: str(), 触发日志的 IP 地址
    :return: None
    """
    now = datetime.datetime.today()

    logger_func = getattr(logger, level)

    location = locate_using_ip_address(ip_address)
    http_header = get_http_header_from_request(request)

    log_data = ("[*] {} 的IP {} 于 {}\n" + str_format).format(location, ip_address, now)
    if len(func_kwargs) > 0:
        log_data += ", 相关参数为: {}\n".format(func_kwargs)
    log_data += "\n{sep} HTTP-HEADER {sep}\n{}".format(http_header, sep="=" * 30)

    email_sender.send_email(message=log_data, ip_address=ip_address, logger=logger, location=location,
                            send_email_check=email_check)
    logger_func(log_data)


@decorator_with_args
def log_wrapper(func, *, str_format="", level="info", logger=None):
    """
    负责进行日志记录的装饰器
    :param func:
    :param str_format:
    :param level:
    :param logger:
    :return:
    """

    @wraps(func)
    def wrapper(request=None, *func_args, **func_kwargs):
        if request is not None:
            # 检查是否要发送邮件
            ip_address = get_ip_from_django_request(request)

            email_check = email_sender.want_to_send_email(ip_address)

            # 记录日志并发送邮件
            make_a_log = threading.Thread(target=background_deal, kwargs={"logger": logger,
                                                                          "level": level,
                                                                          "request": request,
                                                                          "func_kwargs": func_kwargs,
                                                                          "str_format": str_format,
                                                                          "ip_address": ip_address,
                                                                          "email_check": email_check})
            make_a_log.start()

        return func(request, *func_args, **func_kwargs)

    return wrapper


def is_valid_ip(ip_address, *, ip_list=None):
    """
    判断是否为合法的 IP 地址
    :param ip_address: str(), 访问者的 IP, 比如 "127.0.0.1"
    :param ip_list: list(), 允许访问的 IP 列表, 可以是域名, 比如 ["127.0.0.1", "watch0.top"]
    :return: True or False
    """
    if not ip_list:
        ip_list = const.IP_LIMIT

    true_ip_list = list()

    for each in ip_list:
        try:
            each = ipaddress.ip_address(each)
        except ValueError:
            each = ipaddress.ip_address(socket.gethostbyname(each))
        true_ip_list.append(each)

    return ipaddress.ip_address(ip_address) in true_ip_list


@decorator_with_args
def ip_limit(func, *, ip_list=None):
    """
    限定 IP 访问
    :param func:
    :param ip_list: list(), 仅允许列表中的 IP 地址进行访问
    :return:
    """
    if not ip_list:
        ip_list = ["127.0.0.1"]

    @wraps(func)
    def wrapper(request=None, *func_args, **func_kwargs):
        logger.debug("[*] 判断是否允许 IP 访问")
        if request is not None:
            # 检查访问者的 IP 地址
            visitor_ip = get_ip_from_django_request(request)
            logger.debug("[*] 访问者 IP 是 {}".format(visitor_ip))

            # 如果是允许访问的 IP
            if is_valid_ip(visitor_ip, ip_list=ip_list):
                logger.debug("[!] 访问者 {} 允许访问".format(visitor_ip))
                return func(request, *func_args, **func_kwargs)
            else:
                logger.info("[!] 访问者 {} 不允许访问".format(visitor_ip))

        return HttpResponse("[-] 访问权限不足")

    return wrapper


def extract_tag_name_from_path(root_path, file_path):
    """
    从路径中提取 tag 的信息
    :param root_path: str(), 比如 '/Users/L1n/Desktop/Code/Python/my_blog_source/notes'
    :param file_path: str(), 比如 '/Users/L1n/Desktop/Code/Python/my_blog_source/notes/aa/bb/总结笔记-Docker学习.md'
    :return: list(), ("aa", "bb")
    """
    return file_path[len(root_path):].split("/")[1:-1]


def is_static_file_exist(file_name):
    """
    验证文件是否存在
    :param file_name: str(), 比如 "标准正态分布 Z 值表.html"
    :return: True or False
    """
    test_file_name = file_name
    test_file_path = os.path.join(const.STATIC_HTMLS_PATH, test_file_name)
    return os.path.exists(test_file_path)
