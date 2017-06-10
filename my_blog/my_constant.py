#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 定义定义常量类以及整个工程的各个 my_constant 变量

2017.06.10 修正一下 PyCharm 无法找到该文件变量应用的问题 + 添加一个控制记录的 HTTP 字段的变量
2017.06.08 由于之前的方式会导致 PyCharm 无法识别本脚本中的常量名, 因此重构了一下, 现在可以识别的, 不过本脚本会有警告
2017.06.04 添加控制是否进行功能测试的选项
2017.04.30 更新 gitbook 格式
2017.03.15 更新有关搜索框的常量信息
2017.03.06 更新一堆常量信息
2017.01.28 把要传给模板的命名数组作为一个常量放进来了
"""
import os
import sys

from django.conf import settings
from collections import namedtuple

__author__ = '__L1n__w@tch'


class _Const:
    TEMP = "为啥添加了这个变量之后 IDE 就能查找到变量引用了?"

    class ConstError(TypeError):
        pass

    class ConstCaseError(ConstError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't change my_constant.{}".format(name))
        if not name.isupper():
            raise self.ConstCaseError("my_constant name {} is not all uppercase".format(name))
        self.__dict__[name] = value


sys.modules[__name__] = _Const()

import my_constant as const

# const = _Const()
const.EMPTY_ARTICLE_ERROR = "没有相关文章题目"
const.KEYWORD_IN_TITLE = "关键词仅出现标题中"
const.KEYWORD_IN_HREF = "关键词出现在 url 链接中"
const.PLACE_HOLDER = "What are you looking for?"
const.HOME_PAGE_ARTICLES_NUMBERS = 2
const.NOTES_PATH_PARENT_DIR = os.path.dirname(settings.BASE_DIR)
const.ARTICLE_STRUCTURE = namedtuple("article_post", ["note", "content", "type"])
const.MARKDOWN_TREE_STRUCTURE = namedtuple("toc_tree", ["title", "id", "child"])

# 日记页面
const.JOURNAL_NOT_FOUND = "(●￣(ｴ)￣●)那天居然没写日记(O_o)??"

# 吃货页面
const.EATING_MENU_STRUCTURE = namedtuple("eating_menu", ["day_time", "morning", "noon", "night"])

# 调试选项
# git 提交前需要改为 False or True, 要不然网站会跑失败的...
const.SLOW_CONNECT_DEBUG = False  # True if input("是否要访问被墙网站?(yes/no)") == "yes" else False
const.FUNCTION_TEST = True  # True if input("是否进行功能测试?(yes/no)") == "yes" else False

# 发送邮件
const.WANT_SEND_EMAIL = True

# 搜索页面
const.ID_SEARCH_RESULT_TITLE = "id_search_result_title"
const.SEARCH_RESULT_INFO = namedtuple("search_result_info", ["keyword", "content", "linenumber"])
const.SEARCH_CONTENT_HELP_TEXT = "请输入要搜索的内容"
const.SEARCH_CHOICE_HELP_TEXT = "请选择要查询的范围"

# 用来形成博客的文章 git
const.NOTES_PATH_NAME = "notes"
const.ARTICLES_GIT_REPOSITORY = "https://git.oschina.net/w4tch/notes_set.git"
const.NOTES_GIT_PATH = os.path.join(const.NOTES_PATH_PARENT_DIR, const.NOTES_PATH_NAME)

# 用来形成日记的文章 git
const.JOURNALS_PATH_NAME = "journals"
const.JOURNALS_GIT_REPOSITORY = "https://git.oschina.net/w4tch/sxf_notes_set.git"
const.JOURNALS_GIT_PATH = os.path.join(const.NOTES_PATH_PARENT_DIR, const.JOURNALS_PATH_NAME)

# 用来形成 GitBook 的各个仓库
const.GITBOOK_PATH_NAME = "gitbooks"
const.GITBOOK_CODES_PATH = os.path.join(const.NOTES_PATH_PARENT_DIR, const.GITBOOK_PATH_NAME)
const.GITBOOK_USER_NAME = "l1nwatch"
const.GITBOOK_INFO = namedtuple("gitbook_info", ["git_address", "book_name"])
const.GITBOOK_CODES_REPOSITORY = {
    "pythonweb": const.GITBOOK_INFO("https://git.oschina.net/w4tch/PythonWeb.git", "《PythonWeb 开发: 测试驱动方法》"),
}

# URL 相关
const.SEARCH_URL = "/search/"
const.ARTICLE_DISPLAY_URL = "/articles/{}/"
const.JOURNAL_DISPLAY_URL = "/work_journal/{}/"
const.GITBOOK_DISPLAY_URL = "/gitbook_notes/{}/"
const.ARTICLE_UPDATE_URL = "/articles/update_notes/"
const.CATEGORY_SEARCH_URL = "/articles/category{}/"
const.TAG_SEARCH_URL = "/articles/tag{}/"

# 模板相关
const.ARCHIVE_TEMPLATE = "archives.html"
const.TAG_TEMPLATE = "archives.html"
const.CATEGORY_TEMPLATE = "archives.html"

# 记录日志希望记录的 HTTP 字段
const.LOG_HTTP_HEADERS_WHITE_LIST = ["CONTENT_LENGTH", "CONTENT_TYPE", "HTTP_ACCEPT", "HTTP_ACCEPT_ENCODING",
                                     "HTTP_ACCEPT_LANGUAGE", "HTTP_HOST", "HTTP_REFERER", "HTTP_USER_AGENT",
                                     "QUERY_STRING", "REMOTE_ADDR", "REMOTE_HOST", "REMOTE_USER", "REQUEST_METHOD",
                                     "SERVER_NAME", "SERVER_PORT", "HTTP_CONNECTION"]

if __name__ == "__main__":
    pass
