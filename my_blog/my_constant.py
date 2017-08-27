#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 定义定义常量类以及整个工程的各个 my_constant 变量

2017.07.09 新增 summary 结构体, 方便生成 html
2017.07.07 新增 event timeline 结构体, 方便生成 html
2017.06.30 新增 life_summary 相关变量
2017.06.29 新增 timeline 相关变量
2017.06.24 补充 just_eating 的常量
2017.06.23 继续补充 ToolHub 中 A/B Testing 选项卡的常量
2017.06.22 补充 ToolHub 选项卡的常量
2017.06.17 扩展搜索 Tag 函数, 于是修改对应常量
2017.06.16 增加一系列跟 GitBook 有关的变量
2017.06.15 增加一系列跟 ToolHub 有关的变量
2017.06.14 新增有关 toolhub 返回静态 HTML 的变量以及其他用在 ToolHub 代码中的常量
2017.06.10 修正一下 PyCharm 无法找到该文件变量应用的问题 + 添加一个控制记录的 HTTP 字段的变量
2017.06.08 由于之前的方式会导致 PyCharm 无法识别本脚本中的常量名, 因此重构了一下, 现在可以识别的, 不过本脚本会有警告
2017.06.04 添加控制是否进行功能测试的选项
2017.04.30 更新 gitbook 格式
2017.03.15 更新有关搜索框的常量信息
2017.03.06 更新一堆常量信息
2017.01.28 把要传给模板的命名数组作为一个常量放进来了
"""
# 标准库
import os
import sys
from collections import namedtuple

from django.conf import settings

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
const.IP_LIMIT = ["127.0.0.1", "45.76.98.21"]

# 日记页面
const.JOURNAL_NOT_FOUND = "(●￣(ｴ)￣●)那天居然没写日记(O_o)??"

# ====================================================================================================================

# 吃货页面
const.EATING_MENU_STRUCTURE = namedtuple("eating_menu", ["day_time", "morning", "noon", "night"])
const.JUST_EATING_HOME_URL = "/just_eating/"
const.JUST_EATING_SCHOOL_MENU_URL = const.JUST_EATING_HOME_URL + "school"
const.JUST_EATING_SANGFOR_MENU_URL = const.JUST_EATING_HOME_URL + "sangfor"

# ====================================================================================================================

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

# ====================================================================================================================

# GitBook 相关

# GitBook-URL

const.GITBOOK_HOME_URL = "/gitbook_notes/"
const.GITBOOK_UPDATE_URL = const.GITBOOK_HOME_URL + "update_gitbook_codes/"

# 用来形成 GitBook 的各个仓库
const.GITBOOK_PATH_NAME = "gitbooks"
const.GITBOOK_CODES_PATH = os.path.join(const.NOTES_PATH_PARENT_DIR, const.GITBOOK_PATH_NAME)
const.GITBOOK_USER_NAME = "l1nwatch"
const.GITBOOK_INFO = namedtuple("gitbook_info", ["git_address", "book_name", "tag_names"])
const.GITBOOK_CODES_REPOSITORY = {
    "pythonweb": const.GITBOOK_INFO("https://git.oschina.net/w4tch/PythonWeb.git", "《PythonWeb 开发: 测试驱动方法》",
                                    ["Python"]),
}

# ====================================================================================================================

# ToolHub 相关
# 一/二/三级选项卡
const.TOOLHUB_LEVEL_ONE_OPTIONS = ["Encoding&Cipher", "TestTool"]
const.TOOLHUB_LEVEL_TWO_OPTIONS = ["Encoding", "Cipher", "ABTesting"]
const.TOOLHUB_LEVEL_THREE_OPTIONS = ["正态函数分布 Z 值表", "实验样本数计算工具"]
const.TOOLHUB_AB_TESTING_SAMPLE_SIZE_URL = "http://www.evanmiller.org/ab-testing/sample-size.html"

# STATIC 文件路径
const.TEMPLATES_PATH = os.path.join(settings.BASE_DIR, "toolhub", "templates")
const.STATIC_HTMLS_PATH = os.path.join(const.TEMPLATES_PATH, "static_htmls")

# URL 相关
const.SEARCH_URL = "/search/"

# URL - ARTICLE
const.ARTICLE_DISPLAY_URL = "/articles/{}/"
const.ARTICLE_UPDATE_URL = "/articles/update_notes/"
const.CATEGORY_SEARCH_URL = "/articles/category{}/"
const.TAG_SEARCH_URL = "/{}/tag{}/"

const.JOURNAL_DISPLAY_URL = "/work_journal/{}/"
const.GITBOOK_DISPLAY_URL = "/gitbook_notes/{}/"

# URL - TOOLHUB
const.TOOLHUB_HOME_URL = "/tool_hub/"
const.TOOLHUB_STATIC_HTML_URL = const.TOOLHUB_HOME_URL + "html{}"
const.TOOLHUB_GITHUB_PICTURE_TRANSLATE_URL = const.TOOLHUB_HOME_URL + "github_picture_translate/"
const.TOOLHUB_GITHUB_PICTURE_TRANSLATE_DATA_URL = const.TOOLHUB_GITHUB_PICTURE_TRANSLATE_URL + "data"

# 模板相关
const.ARCHIVE_TEMPLATE = "archives.html"
const.TAG_TEMPLATE = "archives.html"
const.CATEGORY_TEMPLATE = "archives.html"

# 记录日志希望记录的 HTTP 字段
const.LOG_HTTP_HEADERS_WHITE_LIST = ["CONTENT_LENGTH", "CONTENT_TYPE", "HTTP_ACCEPT", "HTTP_ACCEPT_ENCODING",
                                     "HTTP_ACCEPT_LANGUAGE", "HTTP_HOST", "HTTP_REFERER", "HTTP_USER_AGENT",
                                     "QUERY_STRING", "REMOTE_ADDR", "REMOTE_HOST", "REMOTE_USER", "REQUEST_METHOD",
                                     "SERVER_NAME", "SERVER_PORT", "HTTP_CONNECTION"]

# ====================================================================================================================

# Timeline App

# -Travel Event Timeline
const.TRAVEL_EVENT_TIMELINE_URL = "/timeline_app/"
const.TRAVEL_EVENT_TIMELINE_TEMPLATE = "travel_event_timeline.html"

const.TRAVEL_EVENT_STRUCTURE = namedtuple("travel_event_structure", ["day", "month", "title", "data"])

# ====================================================================================================================

# app_life_summary App

# life_summary
const.LIFE_SUMMARY_URL = "/life_summary_app/"
const.LIFE_SUMMARY_TEMPLATE = "life_summary.html"

const.LIFE_SUMMARY_SIDEBAR_IDS = ["id_home_page", "link-one", "link-two", "link-three", "link-four", "link-five",
                                  "link-six", "link-seven"]
const.LIFE_SUMMARY_SIDEBAR_NAMES = ["主页", "洗漱用品", "租房", "服装", "电子装备", "生活习惯", "生活用品", "饮食"]
const.LIFE_SUMMARY_SIDEBAR_ITEMS = namedtuple("life_summary_sidebar_items", ["li_id", "div_number", "div_name"])

const.SUMMARY_STRUCTURE = namedtuple("summary_structure", ["div_id", "title", "fields"])
const.SUMMARY_FIELD_STRUCTURE = namedtuple("summary_field_structure", ["title", "notes"])
const.SUMMARY_FIELD_NOTES_STRUCTURE = namedtuple("summary_field_notes_structure", ["style", "content", "sub_notes"])

# ====================================================================================================================


if __name__ == "__main__":
    pass
