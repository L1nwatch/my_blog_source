#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.06.16 新增更新 GitBook 时会更新 Tag 的代码实现
2017.05.21 添加按点击次数排序的相关代码
2017.04.30 由于 gitbook 格式更改, 代码也做相应修改
2017.03.30 给更新函数添加记日记功能
2017.03.26 重构一下搜索代码, form data 合法性在上层做过了, 这里就不做了
2017.03.10 将记录日记的装饰器装饰到对应视图上
2017.03.10 发现 title 字段的 BUG
2017.03.08 开始进行部分重构工作
2017.03.07 新增 form data 的清理工作
2017.03.05 开始编写 GitBook 这个 APP
"""
# 标准库
import logging
import os
import re
import urllib.parse
import pypinyin

from django.shortcuts import redirect

# 自己的模块
from articles.forms import BaseSearchForm
from articles.models import Tag
from common_module.common_help_function import (get_ip_from_django_request, create_search_result,
                                                search_keyword_in_model,
                                                clean_form_data, get_context_data, log_wrapper, is_valid_git_address)
from gitbook_notes.models import GitBook
import my_constant as const

logger = logging.getLogger("my_blog.gitbooks.views")


def get_latest_gitbooks(gitbook_name, address):
    if not is_valid_git_address(address):
        raise RuntimeError("[-] GitBook 地址错误")

    notes_git_path = const.GITBOOK_CODES_PATH

    # 判断是否已经 git 过
    if not os.path.exists(os.path.join(notes_git_path, gitbook_name, ".git")):
        # 确保目录已经建立了
        os.system("mkdir -p {}".format(notes_git_path))

        # 没有 git 过则执行 git clone 操作
        command = ("cd {} && git clone {} {}"
                   .format(notes_git_path, address, gitbook_name))
    else:
        # 如果有 git 过则执行更新操作
        command = "cd {} && git reset --hard && git pull".format(os.path.join(notes_git_path, gitbook_name))
    os.system(command)


def is_valid_md_file(path, file_name, root_path):
    """
    判断是不是要保存进数据库的 md 文件
    :param path: str(), md 文件的绝对路径
    :param file_name: str(), md 文件名
    :param root_path: str(), 根目录的路径
    :return: boolean(), True or False
    """
    # 根目录下的 SUMMARY.md 跳过
    if path == root_path and file_name.lower() == "summary.md".lower():
        return False
    elif file_name.endswith(".md"):
        return True
    return False


def get_right_href(gitbook_name, title):
    """
    计算得到正确的 href
    2017.04.30 修改了一下 GitBook 书名的显示, 结果求取 href 的也受到影响了
    :param gitbook_name: str(), gitbook 书名
    :param title: str(), 文件名路径, 比如 'PythonWeb开发: 测试驱动方法/readme.md'
    :return: str(), 正确的 gitbook href
    """
    user_name = const.GITBOOK_USER_NAME
    result_title = title[:-len(".md")].lower()

    if result_title == "readme":
        href_format = "https://{username}.gitbook.io/{gitbook_name}/"
    else:
        if result_title.endswith("readme"):
            result_title = result_title[:-len("readme")]
        result_title = result_title.replace(":", "").replace(" ", "").replace("_", "")
        temp_title = list()
        for each_split in result_title.split("/"):
            temp_title.append("-".join(pypinyin.lazy_pinyin(each_split)))
        result_title = "/".join(temp_title)
        href_format = "https://{username}.gitbook.io/{gitbook_name}/{result_title}"

    return href_format.format(username=user_name,
                              gitbook_name=urllib.parse.quote(gitbook_name).lower(),
                              result_title=result_title)


def format_title(title, book_name):
    """
    主要是针对书名已经存在于 title 的情况进行处理, 还有就是 readme 的去除, 这里进行清除操作
    对有无书名的判断会清除空白符后进行判断
    :param title: str(), 比如 "PythonWeb开发: 测试驱动方法/准备工作和应具备的知识/readme"
    :param book_name: str(), 比如 "《PythonWeb 开发:测试驱动开发》"
    :return: str(), 格式化过后的 title, 比如 "《PythonWeb 开发:测试驱动开发》-准备工作和应具备的知识"
    """
    title = title.lower()

    # 含有书名
    if "/" in title:
        book_name_without_symbol = book_name.lower().strip("《》")
        book_name_without_white = book_name_without_symbol.replace(" ", "").replace("\t", "")
        title_book_name, title_path = title.split("/", maxsplit=1)
        if book_name_without_white == title_book_name.replace(" ", "").replace("\t", ""):
            title = title_path

    # 去除 readme
    if title.endswith("readme"):
        title = title[:-len("readme")]
        title = title.rstrip("/")

    if title != "":
        return "{}-{}".format(book_name, title)
    else:
        return book_name


def get_title_and_md_file_name(title, display_book_name):
    """
    根据给定的从 summary.md 中获取的 title 来生成 title 和 md_file_name 字段
    :param title: str(), 比如 "网易 2017 校招笔试编程题/二进制权重.md"
    :param display_book_name: str(), 显示用的 GitBook 名字, 比如 "《PythonWeb 开发:测试驱动开发》"
    :return: tuple, (title, md_file_name), 比如 ("《PythonWeb 开发:测试驱动开发》-网易 2017 校招笔试编程题/二进制权重", "二进制权重.md")
    """
    # 获取 md 名
    if "/" in title:
        md_file_name = title.rsplit("/", maxsplit=1)[1]
    else:
        md_file_name = title

    # 获取 title
    title_save_to_db = title[:-len(".md")]  # 去除后缀名 .md

    # 判断书名是否已经存在于 title 之中, 存在则去掉
    title_save_to_db = format_title(title_save_to_db, display_book_name)

    return title_save_to_db, md_file_name


def sync_database(title, gitbook_name, gitbook_info):
    """
    进行同步数据库的操作, 即会保存最新内容, 如果是不存在的则会进行创建操作
    :param title: str(), 要放进数据库的每一章的路径, 比如 "'PythonWeb开发: 测试驱动方法/readme.md'"
    :param gitbook_name: str(), gitbook 的名字
    :param gitbook_info: namedtuple(), 保存 GitBook 的相关信息
    :return: str(), 所操作的 title
    """
    root_path = "{}/{}".format(const.GITBOOK_CODES_PATH, gitbook_name)

    title_save_to_db, md_file_name = get_title_and_md_file_name(title, gitbook_info.book_name)

    right_href = get_right_href(gitbook_name, title)
    gitbook_tags = [Tag.objects.get_or_create(tag_name=x)[0] for x in gitbook_info.tag_names]
    with open("{}/{}".format(root_path, title), "r") as f:
        gitbook_content = f.read()

    try:
        # 已经存在
        gitbook = GitBook.objects.get(href=right_href)
        # 文件内容有所改动
        if gitbook_content != gitbook.content:
            gitbook.content = gitbook_content
        # md 文件名变了
        if md_file_name != gitbook.md_file_name:
            gitbook.md_file_name = md_file_name
        # title 变化了
        if title_save_to_db != gitbook.title:
            gitbook.title = title_save_to_db
    except GitBook.DoesNotExist:
        # 不存在
        gitbook = GitBook.objects.create(title=title_save_to_db, content=gitbook_content,
                                         md_file_name=md_file_name, book_name=gitbook_name,
                                         href=right_href)

    # 同步最新的 Tag
    if gitbook_tags != gitbook.tag:
        gitbook.tag = gitbook_tags
    gitbook.save()

    return title_save_to_db


def get_title_list_from_summary(summary_path):
    """
    从 summary_path 提取出每一篇的 title
    :param summary_path: str(), summary.md 的路径
    :return: list(), 每个元素是个要放进数据库的 title
    """
    result_list = list()
    title_re = re.compile("\[.*\]\((.*)\)")

    with open(summary_path, "r") as f:
        for each_line in f:
            re_result = title_re.findall(each_line)
            if re_result:
                result_list.append(re_result[0])

    return result_list


def get_summary_path(gitbook_name):
    """
    获取对应的 summary.md 的路径, 主要是担心名字大小写问题导致文件读取不到
    :param gitbook_name: str(), gitbook 的名字
    :return: str(), summary.md 的绝对路径, 比如 "'/Users/.../my_blog_source/gitbooks/PythonWeb/SUMMARY.md'"
    """
    root_path = os.path.join(const.GITBOOK_CODES_PATH, gitbook_name)
    for each_file in os.listdir(root_path):
        if each_file.lower() == "summary.md":
            return os.path.join(root_path, each_file)
    raise RuntimeError


def update_gitbook_db(gitbook_name, gitbook_info):
    """
    更新 gitbook 数据到数据库中
    :param gitbook_name: str(), gitbook 的名字, 比如 "PythonWeb"
    :param gitbook_info: namedtuple(), 保存 GitBook 的相关信息
    :return: set(), 包含存进数据库的每一章笔记
    """
    notes_in_git = set()

    summary_path = get_summary_path(gitbook_name)

    # 读取 root 目录下的 SUMMARY.md, 提取出每一篇标题的路径
    title_list = get_title_list_from_summary(summary_path)
    for each_title in title_list:
        # 进行同步数据库的操作
        title = sync_database(each_title, gitbook_name, gitbook_info)
        notes_in_git.add(title)

    return notes_in_git


@log_wrapper(str_format="更新 gitbook 笔记", logger=logger)
def update_gitbook_codes(request=None):
    """
    2017.03.05 开始实现 gitbook 数据写入数据库的代码
    2016.10.30 实现 git clone && pull 功能
    """
    gitbook_category_dict = const.GITBOOK_CODES_REPOSITORY

    for gitbook_name, gitbook_info in gitbook_category_dict.items():
        try:
            # 获取最新的 gitbook 代码
            get_latest_gitbooks(gitbook_name, gitbook_info.git_address)

            # 更新到数据库中
            notes_in_git = update_gitbook_db(gitbook_name, gitbook_info)

            for each_note_in_db in GitBook.objects.filter(book_name=gitbook_name):
                if each_note_in_db.title not in notes_in_git:
                    each_note_in_db.delete()
        except Exception as e:
            logger.error("[-] 更新 GitBook 代码出现错误: {}".format(str(e)))

    return redirect("/")


@log_wrapper(str_format="进行了 GitBooks 搜索", logger=logger)
def do_gitbooks_search(request):
    """
    2017.02.08 参考搜索文章的代码, 写了这个搜索日记的代码
    :param request: django 传给视图函数的参数 request, 包含 HTTP 请求的各种信息
    """

    if request.method == "POST":
        form = BaseSearchForm(data=request.POST)
        search_text = clean_form_data(form.data["search_content"])
        # 按关键词来搜索
        keywords = set(search_text.split(" "))

        gitbook_list = search_keyword_in_model(keywords, GitBook, ["content"])

        context_data = get_context_data(request, "gitbooks",
                                        {'post_list': create_search_result(gitbook_list, keywords, "gitbook_notes"),
                                         'error': None, "form": form})
        context_data["error"] = const.EMPTY_ARTICLE_ERROR if len(gitbook_list) == 0 else False

        return context_data


@log_wrapper(str_format="查看了 GitBook", logger=logger)
def gitbook_display(request, gitbook_id):
    """
    接收 gitbook_id 然后跳转到对应的 href 进行 GitBook 显示
    :param request: 发送给视图函数的请求
    :param gitbook_id: 请求的 gitbook id
    """
    gitbook = GitBook.objects.get(id=gitbook_id)
    logger.info("ip: {} 查看 gitbook: {}".format(get_ip_from_django_request(request), gitbook.title))

    if request.method == "POST" and request.POST["visited"] == "True":
        gitbook.click_times += 1
        gitbook.save()

    return redirect(gitbook.href)
