#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 定义定义常量类以及整个工程的各个 const 变量
"""
import os

from django.conf import settings

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
const.PLACE_HOLDER = "word to search"
const.HOME_PAGE_ARTICLES_NUMBERS = 2
const.SLOW_CONNECT_DEBUG = True if input("是否要访问被墙网站?(yes/no)") == "yes" else False
const.NOTES_PATH_PARENT_DIR = os.path.dirname(settings.BASE_DIR)

# 用来形成博客的文章 git
const.NOTES_PATH_NAME = "notes"
const.ARTICLES_GIT_REPOSITORY = "https://github.com/L1nwatch/notes_set.git"
const.NOTES_GIT_PATH = os.path.join(const.NOTES_PATH_PARENT_DIR, const.NOTES_PATH_NAME)

# 用来形成 GitBook 的各个仓库
const.GITBOOK_PATH_NAME = "gitbook_notes"
const.GITBOOK_CODES_PATH = os.path.join(const.NOTES_PATH_PARENT_DIR, const.GITBOOK_PATH_NAME)
const.GITBOOK_CODES_REPOSITORY = {
    "interview_collect": "https://github.com/L1nwatch/interview_collect.git",
    "PythonWeb": "https://github.com/L1nwatch/PythonWeb.git",
    # "it_people_healthy": "https://github.com/L1nwatch/it_people_healthy.git",
    "writing_solid_python_code_gitbook": "https://github.com/L1nwatch/writing_solid_python_code_gitbook.git",
    "CTF": "https://github.com/L1nwatch/CTF.git",
}

if __name__ == "__main__":
    pass
