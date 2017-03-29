# -*- coding: utf-8 -*-
# version: Python3.X
""" code_collect 的视图函数

2017.03.29 新增 do_code_search 视图函数, 不过还没编写对应的测试, 先把 code_collect 的测试通过了再说吧
2017.03.28 新增一个 code_collect 视图函数, 用于更新数据库信息
"""
from articles.models import Article
from gitbook_notes.models import GitBook
from work_journal.models import Journal
from code_collect.models import CodeCollect

from django.shortcuts import redirect
from articles.common_help_function import log_wrapper, get_ip_from_django_request

import logging
import re

logger = logging.getLogger("my_blog.code_collect.views")


@log_wrapper(str_format="进行了代码块的搜索", logger=logger)
def do_code_search(request):
    """
    负责实现代码块的搜索功能
    :param request:
    :return:
    """
    return redirect("home")


def get_all_code_type_in_note(note):
    """
    读取 note 里的内容, 提取出里面有的代码段
    :param note: model.objects 实例
    :return: list(), 包含了这篇笔记所含有的代码段, 比如 ["python", "c++", ...]
    """
    result_list = list()
    code_type_re = re.compile("```(.+)", flags=re.IGNORECASE)

    for each_line in note.content.splitlines():
        re_result = code_type_re.findall(each_line)
        if re_result:
            result_list.append(re_result[0])

    return result_list


def sync_code_db(each_note_db):
    """
    实现更新操作
    :param each_note_db: model 实例, 比如 Article、Journal、GitBook
    :return: None, 将操作结果直接更新到数据库中
    """
    # 遍历每篇笔记
    for each_note in each_note_db.objects.all():
        # 获取每篇笔记中包含的 code_type
        all_code_type = get_all_code_type_in_note(each_note)

        # 为每份 code_type 创建一条记录
        for each_code_type in all_code_type:
            code, created = CodeCollect.objects.get_or_create(note=each_note, code_type=each_code_type)

        # 清除多余的 code_type
        for each_code in CodeCollect.objects.filter(note=each_note):
            if each_code.code_type not in all_code_type:
                each_code.delete()


def code_collect(request=None):
    """
    负责实现代码块信息的收集, 之后保存到数据库中
    :param request: django request, 可有可无, 毕竟这不是用来前端 URL 映射的
    :return: None
    """
    # request 不为 None 时才记日记
    if request:
        logger.info("[*] {} 使用了 code_collect 视图函数".format(get_ip_from_django_request(request)))

    # 依次更新 Article、Journal、GitBook
    for each_note_db in [Article, Journal, GitBook]:
        sync_code_db(each_note_db)

    return redirect("home")
