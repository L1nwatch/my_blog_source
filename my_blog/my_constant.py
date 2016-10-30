#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 定义定义常量类以及整个工程的各个 const 变量
"""
# import sys

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
const.ARTICLES_GIT_REPOSITORY = "https://github.com/L1nwatch/notes_set.git"
const.HOME_PAGE_ARTICLES_NUMBERS = 2
const.DEBUG_GIT = True if input("确定要进行 git 测试(慢)?(yes/no)") == "yes" else False
const.NOTES_PATH_NAME = "notes"

if __name__ == "__main__":
    pass
