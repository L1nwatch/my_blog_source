#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.04.30 由于 gitbook 格式更改, 代码也做相应修改
2017.03.30 给更新函数添加记日记功能
2017.03.26 重构一下搜索代码, form data 合法性在上层做过了, 这里就不做了
2017.03.10 将记录日记的装饰器装饰到对应视图上
2017.03.10 发现 title 字段的 BUG
2017.03.08 开始进行部分重构工作
2017.03.07 新增 form data 的清理工作
2017.03.05 开始编写 GitBook 这个 APP
"""
import os
import re
import logging
import urllib.parse

# 以下为 django 相关的库

from articles.common_help_function import (get_ip_from_django_request, create_search_result, search_keyword_in_model,
                                           clean_form_data, get_context_data, log_wrapper, is_valid_git_address)
from articles.forms import BaseSearchForm
from my_constant import const
from gitbook_notes.models import GitBook

from django.shortcuts import redirect

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


def get_right_href(gitbook_name, title, md_file_name):
    """
    计算得到正确的 href
    :param gitbook_name: str(), gitbook 书名
    :param title: str(), 正确的 URI 路径
    :param md_file_name: str(), 正确的 md 文件名
    :return: str(), 正确的 gitbook href
    """
    user_name = const.GITBOOK_USER_NAME
    md_file_name = md_file_name.rsplit(".md", maxsplit=1)[0]

    if title.lower() == "readme":
        href_format = "https://{username}.gitbooks.io/{gitbook_name}/content/index.html"
    elif title == md_file_name:
        href_format = "https://{username}.gitbooks.io/{gitbook_name}/content/{title}.html"
    elif "/" in title:
        if md_file_name == title.rsplit("/", maxsplit=1)[1]:
            href_format = "https://{username}.gitbooks.io/{gitbook_name}/content/{title}.html"
        else:
            href_format = "https://{username}.gitbooks.io/{gitbook_name}/content/{title}/{md_file_name}.html"
    else:
        href_format = "https://{username}.gitbooks.io/{gitbook_name}/content/{title}/{md_file_name}.html"

    return href_format.format(username=user_name,
                              gitbook_name=urllib.parse.quote(gitbook_name).lower(),
                              title=urllib.parse.quote(title),
                              md_file_name=urllib.parse.quote(md_file_name))


def get_title_and_md_file_name(title):
    """
    根据给定的从 summary.md 中获取的 title 来生成 title 和 md_file_name 字段
    :param title: str(), 比如 "网易 2017 校招笔试编程题/二进制权重.md"
    :return: tuple, (title, md_file_name), 比如 ("网易 2017 校招笔试编程题/二进制权重", "二进制权重.md")
    """
    if "/" in title:
        title_save_to_db = str(title).rstrip(".md")
        # 这一步主要是用来去除 readme 的, 比如 "PythonWeb开发: 测试驱动方法/readme"
        # 得把 readme 去掉, 仅保留 / 前面的内容, 比如 "PythonWeb开发: 测试驱动方法"
        pre_path, final_name = title_save_to_db.rsplit("/", maxsplit=1)
        if final_name.lower() == "readme":
            title_save_to_db = pre_path
        md_file_name = str(title).rsplit("/", maxsplit=1)[1]
    else:
        title_save_to_db, md_file_name = title.rstrip(".md"), title
    return title_save_to_db, md_file_name


def sync_database(title, gitbook_name):
    """
    进行同步数据库的操作, 即会保存最新内容, 如果是不存在的则会进行创建操作
    :param title: str(), 要放进数据库的每一章的路径, 比如 ""
    :param gitbook_name: str(), gitbook 的名字
    :return: str(), 所操作的 title
    """
    root_path = "{}/{}".format(const.GITBOOK_CODES_PATH, gitbook_name)

    title_save_to_db, md_file_name = get_title_and_md_file_name(title)

    right_href = get_right_href(gitbook_name, title_save_to_db, md_file_name)
    with open("{}/{}".format(root_path, title), "r") as f:
        gitbook_content = f.read()

    try:
        # 已经存在
        gitbook = GitBook.objects.get(title=title_save_to_db)
        # 文件内容有所改动
        if gitbook_content != gitbook.content:
            gitbook.content = gitbook_content
        # md 文件名变了
        if md_file_name != gitbook.md_file_name:
            gitbook.md_file_name = md_file_name
        # href 变化了
        if right_href != gitbook.href:
            gitbook.href = right_href
        gitbook.save()
    except GitBook.DoesNotExist:
        # 不存在
        GitBook.objects.create(title=title_save_to_db, content=gitbook_content,
                               md_file_name=md_file_name, book_name=gitbook_name,
                               href=right_href)

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


def update_gitbook_db(gitbook_name):
    """
    更新 gitbook 数据到数据库中
    :param gitbook_name: str(), gitbook 的名字, 比如 "PythonWeb"
    :return: set(), 包含存进数据库的每一章笔记
    """
    notes_in_git = set()

    summary_path = get_summary_path(gitbook_name)

    # 读取 root 目录下的 SUMMARY.md, 提取出每一篇标题的路径
    title_list = get_title_list_from_summary(summary_path)
    for each_title in title_list:
        # 进行同步数据库的操作
        title = sync_database(each_title, gitbook_name)
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
            notes_in_git = update_gitbook_db(gitbook_name)

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
    return redirect(gitbook.href)
