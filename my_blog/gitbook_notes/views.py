#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.03.05 开始编写 GitBook 这个 APP
"""
import os
import re
import logging
import urllib.parse

# 以下为 django 相关的库

from articles.common_help_function import get_ip_from_django_request, create_search_result
from articles.forms import BaseSearchForm
from my_constant import const
from gitbook_notes.models import GitBook

from django.shortcuts import redirect
from django.http import Http404

logger = logging.getLogger("my_blog.gitbooks.views")


def _get_context_data(update_data=None):
    """
    定制要发送给模板的相关数据
    :param update_data: 以需要发送给 base.html 的数据为基础, 需要额外发送给模板的数据
    :return: dict(), 发送给模板的全部数据
    """
    data_return_to_base_template = {"form": BaseSearchForm(), "is_valid_click": "True",
                                    "gitbooks_numbers": len(GitBook.objects.all()), "current_type": "gitbook_notes"}
    if update_data is not None:
        data_return_to_base_template.update(update_data)

    return data_return_to_base_template


def get_latest_gitbooks(gitbook_name, address):
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

    href_format = "https://{username}.gitbooks.io/{gitbook_name}/content/{title}/{md_file_name}.html"

    return href_format.format(username=user_name,
                              gitbook_name=urllib.parse.quote(gitbook_name).lower(),
                              title=urllib.parse.quote(title),
                              md_file_name=urllib.parse.quote(md_file_name))


def sync_database(title, gitbook_name):
    """
    进行同步数据库的操作, 即会保存最新内容, 如果是不存在的则会进行创建操作
    :param title: str(), 要放进数据库的每一章的路径
    :param gitbook_name: str(), gitbook 的名字
    :return: str(), 所操作的 title
    """
    root_path = "{}/{}".format(const.GITBOOK_CODES_PATH, gitbook_name)
    title_save_to_db, md_file_name = str(title).rsplit("/", maxsplit=1)
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


def update_gitbook_db(gitbook_name):
    """
    更新 gitbook 数据到数据库中
    :param gitbook_name: str(), gitbook 的名字, 比如 "PythonWeb"
    :return: set(), 包含存进数据库的每一章笔记
    """
    notes_in_git = set()

    summary_path = os.path.join(const.GITBOOK_CODES_PATH, gitbook_name, "summary.md")

    # 读取 root 目录下的 SUMMARY.md, 提取出每一篇标题的路径
    title_list = get_title_list_from_summary(summary_path)
    for each_title in title_list:
        # 进行同步数据库的操作
        title = sync_database(each_title, gitbook_name)
        notes_in_git.add(title)

    return notes_in_git


def update_gitbook_codes(request=None):
    """
    2017.03.05 开始实现 gitbook 数据写入数据库的代码
    2016.10.30 实现 git clone && pull 功能
    """
    gitbook_category_dict = const.GITBOOK_CODES_REPOSITORY

    for gitbook_name, address in gitbook_category_dict.items():
        # 获取最新的 gitbook 代码
        get_latest_gitbooks(gitbook_name, address)

        # 更新到数据库中
        notes_in_git = update_gitbook_db(gitbook_name)

        for each_note_in_db in GitBook.objects.filter(book_name=gitbook_name):
            if each_note_in_db.title not in notes_in_git:
                each_note_in_db.delete()

    return redirect("/")


def do_gitbooks_search(request):
    """
    2017.02.08 参考搜索文章的代码, 写了这个搜索日记的代码
    :param request: django 传给视图函数的参数 request, 包含 HTTP 请求的各种信息
    """

    def __search_keyword_in_gitbooks(keyword_set):
        result_set = set()
        first_time = True

        # 对每个关键词进行处理
        for each_key_word in keyword_set:
            # 获取上一次过滤剩下的文章列表, 如果是第一次则为全部文章
            if first_time:
                first_time = False
                articles_from_content_filter = GitBook.objects.filter(content__icontains=each_key_word)

                result_set.update(articles_from_content_filter)
            else:
                temp_result_set = set()
                # 对每篇文章进行查找, 先查找标题, 然后查找内容
                each_key_word = each_key_word.lower()
                for each_article in result_set:
                    if each_key_word in each_article.content.lower():
                        temp_result_set.add(each_article)

                result_set = temp_result_set

        return result_set

    def __form_is_valid_and_ignore_exist_article_error(my_form):
        """
        2016.10.11 重定义验证函数, 不再使用简单的 form.is_valid, 原因是执行搜索的时候发现不能搜索跟已存在的文章一模一样的标题关键词
        :param my_form: form = JournalForm(data=request.POST)
        :return: boolean, True or False
        """
        if my_form.is_valid() is True:
            return True
        elif len(my_form.errors) == 1 and "具有 Title 的 Article 已存在。" in str(my_form.errors):
            return True
        return False

    if request.method == "POST":
        form = BaseSearchForm(data=request.POST)
        # 因为自定义无视某个错误所以不能用 form.cleaned_data["title"], 详见下面这个验证函数
        if __form_is_valid_and_ignore_exist_article_error(form):
            search_text = form.data["title"]
            # 按关键词来搜索
            keywords = set(search_text.split(" "))

            journal_list = __search_keyword_in_gitbooks(keywords)
            logger.info("ip: {} 搜索 GitBook: {}"
                        .format(get_ip_from_django_request(request), form.data["title"]))

            context_data = _get_context_data(
                {'post_list': create_search_result(journal_list, keywords, "gitbook_notes"),
                 'error': None, "form": form})
            context_data["error"] = const.EMPTY_ARTICLE_ERROR if len(journal_list) == 0 else False

            return context_data


def gitbook_display(request, gitbook_id):
    """
    接收 gitbook_id 然后跳转到对应的 href 进行 GitBook 显示
    :param request: 发送给视图函数的请求
    :param gitbook_id: 请求的 gitbook id
    """
    gitbook = GitBook.objects.get(id=gitbook_id)
    logger.info("ip: {} 查看 gitbook: {}".format(get_ip_from_django_request(request), gitbook.title))
    return redirect(gitbook.href)
