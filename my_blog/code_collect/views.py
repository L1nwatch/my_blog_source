# -*- coding: utf-8 -*-
# version: Python3.X
""" code_collect 的视图函数

2017.03.30 继续完成 do_code_search 相关代码, 给更新函数添加记日记功能
2017.03.29 新增 do_code_search 视图函数, 不过还没编写对应的测试, 先把 code_collect 的测试通过了再说吧
2017.03.28 新增一个 code_collect 视图函数, 用于更新数据库信息
"""
from articles.models import Article, BaseModel
from articles.forms import BaseSearchForm
from gitbook_notes.models import GitBook
from work_journal.models import Journal
from code_collect.models import CodeCollect
from my_constant import const

from django.shortcuts import redirect
from articles.common_help_function import (log_wrapper, get_ip_from_django_request,
                                           clean_form_data, get_context_data, create_search_result)

import logging
import re

logger = logging.getLogger("my_blog.code_collect.views")


@log_wrapper(str_format="进行了代码块的搜索", logger=logger)
def do_code_search(request):
    """
    负责实现代码块的搜索功能
    :param request: django request 请求
    :return:
    """
    if request.method == "POST":
        form = BaseSearchForm(request.POST)

        keyword_set, code_type = parse_query(clean_form_data(form.data["search_content"]))

        # 用户指定了要查询的 code_type
        if code_type != "":
            note_set = CodeCollect.objects.filter(code_type=code_type)
        else:
            note_set = CodeCollect.objects.all()

        # 对每篇笔记进行搜索
        result_list = search_code_keyword_in_note_set(note_set, keyword_set, code_type)

        # 为每个搜索结果创建相关信息, 以便展示到前端
        context_data = get_context_data(request, "code",
                                        {'post_list': result_list,
                                         'error': None, "form": form})
        context_data["error"] = const.EMPTY_ARTICLE_ERROR if len(result_list) == 0 else False

        return context_data


def search_code_keyword_in_note(note, keyword_set, all_code_area):
    """
    在某篇特定笔记中查找所有代码块, 如果查询的所有关键词都存在, 则加入结果列表
    :param note: note 实例
    :param keyword_set: set(), 用户查询关键词集合
    :param all_code_area: list(), 包含了该笔记中所有的代码块
    :return: list(), 搜索结果
    """
    result_list = list()

    for each_keyword in keyword_set:
        found = False
        for each_code in all_code_area:
            for i, each_line in enumerate(each_code.splitlines()):
                if str(each_keyword).lower() in each_line.lower():
                    result_list.append(const.SEARCH_RESULT_INFO(each_keyword, each_line, i + 1))
                    found = True
        if not found:
            result_list.clear()

    return result_list


def search_code_keyword_in_note_set(note_set, keyword_set, code_type):
    """
    在所有笔记的代码块中进行搜索
    :param note_set: set(), 笔记集合, 要查询就从这份集合里面查询
    :param keyword_set: set(), 每个元素是 str(), 表明要查询的关键词, 比如 {"print", "Hello"}
    :param code_type: str(), 表明要搜索的代码语言, 比如 "python" 就只搜 Python 语言的
    :return: list(), 每一个元素都是一个命名元组, 每一个元素的格式类似于: (id, title, content)
    """
    result_list = list()

    # 过滤一下集合, 确保每篇笔记都含有所有要查询的关键词
    for each_keyword in keyword_set:
        note_set = note_set.filter(note__content__icontains=each_keyword)

    # 遍历集合中的每份笔记
    for each_note in note_set:
        each_note = each_note.note
        # 提取笔记中的每个代码块
        all_code_area = get_all_code_area(each_note, code_type)

        # 搜索是否存在关键词, 所有关键词都有则加入到 result_list 中
        search_result = search_code_keyword_in_note(each_note, keyword_set, all_code_area)

        if search_result:
            result_list.append(const.ARTICLE_STRUCTURE(
                each_note.id, each_note.title, search_result, get_note_type(each_note)
            ))

    return result_list


def get_all_code_area(note, code_type):
    """
    获取笔记中符合 code_type 的所有代码块
    :param note: note 实例
    :param code_type: str(), 比如 "python", 表明只获取 python 代码块
    :return: list(), 每一个元素是该篇笔记的代码块, 比如 ['print("HelloWorld")']
    """
    code_area_re = re.compile("```([^\s]+)([\s\S]*?\n)```", flags=re.IGNORECASE)
    result_list = list()

    re_result = code_area_re.findall(note.content)
    if re_result:
        for each_code_area in re_result:
            if code_type == "":
                result_list.append(each_code_area[1].strip())
            elif code_type.lower() == each_code_area[0].lower():
                result_list.append(each_code_area[1].strip())

    return result_list


def get_note_type(note):
    """
    获取笔记类型, 即判断是 Article、Journal 还是 GitBook
    :param note: note 实例
    :return: str(), 表明笔记类型, 比如 "article", "journals", ...
    """
    if isinstance(note, Article):
        return "articles"
    elif isinstance(note, GitBook):
        return "gitbooks"
    elif isinstance(note, Journal):
        return "journals"
    elif isinstance(note, CodeCollect):
        return "code"
    elif isinstance(note, BaseModel) and hasattr(note, "article"):
        return "articles"
    elif isinstance(note, BaseModel) and hasattr(note, "gitbook"):
        return "gitbooks"
    elif isinstance(note, BaseModel) and hasattr(note, "journal"):
        return "journals"
    else:
        raise RuntimeError("[-] Get note type 出现错误: {}".format(note))


def parse_query(raw_data):
    """
    解析用户发出的查询词
    :param raw_data: str(), 比如 "python aaaa", 表明要搜索 python 代码块中的 aaa 字符串
    :return: tuple(), (set, str), 前者为关键词集合, 后者为 code_type
    """
    code_type = str()
    keyword_set = set()

    # 如果含有空格, 说明第一个空格前的为 code_type
    if " " in raw_data:
        code_type, query = str(raw_data).split(" ", maxsplit=1)
    else:
        query = raw_data

    # 提取关键词 set
    for each_keyword in query.split(" "):
        keyword_set.add(each_keyword)

    return keyword_set, code_type.lower()


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


@log_wrapper(str_format="使用了 code_collect 视图函数", logger=logger)
def code_collect(request=None):
    """
    负责实现代码块信息的收集, 之后保存到数据库中
    :param request: django request, 可有可无, 毕竟这不是用来前端 URL 映射的
    :return: None
    """
    # 依次更新 Article、Journal、GitBook
    for each_note_db in [Article, Journal, GitBook]:
        sync_code_db(each_note_db)

    return redirect("home")
