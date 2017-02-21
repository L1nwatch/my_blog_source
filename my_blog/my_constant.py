#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 定义定义常量类以及整个工程的各个 const 变量

2017.01.28 把要传给模板的命名数组作为一个常量放进来了
"""
import os

from django.conf import settings
from collections import namedtuple

__author__ = '__L1n__w@tch'


class _Const:
    class ConstError(TypeError):
        pass

    class ConstCaseError(ConstError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't change const.{}".format(name))
        if not name.isupper():
            raise self.ConstCaseError("const name {} is not all uppercase".format(name))
        self.__dict__[name] = value


# sys.modules[__name__] = _Const()
const = _Const()
const.EMPTY_ARTICLE_ERROR = "没有相关文章题目"
const.KEYWORD_IN_TITLE = "关键词仅出现标题中"
const.KEYWORD_IN_HREF = "关键词出现在 url 链接中"
const.PLACE_HOLDER = "What are you looking for?"
const.HOME_PAGE_ARTICLES_NUMBERS = 2
const.NOTES_PATH_PARENT_DIR = os.path.dirname(settings.BASE_DIR)
const.ARTICLE_STRUCTURE = namedtuple("article_post", ["id", "title", "content", "type"])
const.MARKDOWN_TREE_STRUCTURE = namedtuple("toc_tree", ["title", "id", "child"])

# 日记页面
const.JOURNAL_NOT_FOUND = "(●￣(ｴ)￣●)那天居然没写日记(O_o)??"

# 调试选项
# git 提交前需要改为 False or True, 要不然网站会跑失败的...
const.SLOW_CONNECT_DEBUG = False  # True if input("是否要访问被墙网站?(yes/no)") == "yes" else False

# 搜索页面
const.ID_SEARCH_RESULT_TITLE = "id_search_result_title"

# 用来形成博客的文章 git
const.NOTES_PATH_NAME = "notes"
const.ARTICLES_GIT_REPOSITORY = "https://git.oschina.net/w4tch/notes_set.git"
const.NOTES_GIT_PATH = os.path.join(const.NOTES_PATH_PARENT_DIR, const.NOTES_PATH_NAME)

# 用来形成日记的文章 git
const.JOURNALS_PATH_NAME = "journals"
const.JOURNALS_GIT_REPOSITORY = "https://git.oschina.net/w4tch/sxf_notes_set.git"
const.JOURNALS_GIT_PATH = os.path.join(const.NOTES_PATH_PARENT_DIR, const.JOURNALS_PATH_NAME)

# 用来形成 GitBook 的各个仓库
const.GITBOOK_PATH_NAME = "gitbook_notes"
const.GITBOOK_CODES_PATH = os.path.join(const.NOTES_PATH_PARENT_DIR, const.GITBOOK_PATH_NAME)
const.GITBOOK_CODES_REPOSITORY = {
    # "interview_collect": "https://github.com/L1nwatch/interview_collect.git",
    "PythonWeb": "https://git.oschina.net/w4tch/PythonWeb.git",
    # "it_people_healthy": "https://github.com/L1nwatch/it_people_healthy.git",
    # "writing_solid_python_code_gitbook": "https://github.com/L1nwatch/writing_solid_python_code_gitbook.git",
    # "CTF": "https://github.com/L1nwatch/CTF.git",
}

if __name__ == "__main__":
    pass
