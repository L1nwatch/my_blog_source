#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 作为测试基类

2017.06.04 继续重构创建测试数据的基类
2017.05.21 为 Article 构造函数添加字段 click_times
2017.04.03 重构一下创建测试数据的代码, 将其分离出来单独作为一个基类了
"""
# 标准库
import datetime
import os
import string
import random

from django.test import TestCase
from django.conf import settings

# 自己的模块
from articles.models import Article, SearchModel, Tag
from articles.views import get_right_content_from_file
from work_journal.models import Journal
from gitbook_notes.models import GitBook
from code_collect.models import CodeCollect
from my_constant import const

__author__ = '__L1n__w@tch'

search_url = "/search/"
article_display_url = "/articles/{}/"
journal_display_url = "/work_journal/{}/"
gitbook_display_url = "/gitbook_notes/{}/"


class CreateTestData:
    """
    负责实现基本的创建测试数据操作, 比如说创建 Article、Journal、GitBook、Code
    """

    @staticmethod
    def get_random_string(length):
        """
        获得一个随机的字符串
        :param length: int(), 字符串长度, 比如 10
        :return: str(), 随机字符串, 比如 "absdadsdsa"
        """
        result = "".join([random.choice(string.ascii_letters) for j in range(length)])
        return result

    def create_article(self, title=None, content=None, category=None, click_times=None):
        if not title:
            title = "{}_{}".format("articles", self.get_random_string(10))
        if not content:
            content = "content"
        if not category:
            category = "category"
        if not click_times:
            click_times = 0
        return Article.objects.create(title=title, content=content, category=category, click_times=click_times)

    def create_journal(self, title=None, content=None, date=None, category=None, click_times=None):
        if not title:
            title = self.get_random_string(10)
        if not content:
            content = "test journal"
        if not date:
            date = datetime.datetime.today() + datetime.timedelta(days=random.randint(0, 365))
        if not category:
            category = "category"
        if not click_times:
            click_times = 0
        return Journal.objects.create(title=title, date=date, content=content, category=category,
                                      click_times=click_times)

    def create_gitbook(self, book_name=None, href=None, md_file_name=None, title=None, content=None, click_times=None):
        if not book_name:
            book_name = "test_book_name"
        if not href:
            href = "http://{}/{}.html".format("test_book_name", self.get_random_string(10))
        if not md_file_name:
            md_file_name = "test.md"
        if not title:
            title = "test_book_name/{}".format(self.get_random_string(10))
        if not content:
            content = "test content"
        if not click_times:
            click_times = 0

        gitbook = GitBook.objects.create(
            book_name=book_name,
            href=href,
            md_file_name=md_file_name,
            title=title,
            content=content,
            click_times=click_times,
        )

        return gitbook

    def create_code(self, note=None, code_type=None):
        if not code_type:
            code_type = "Others"
        if not note:
            note = self.create_article()
        return CodeCollect.objects.create(code_type=code_type, note=note)

    def create_func_map(self, types):
        """
        对创建函数进行映射
        :param types: str(), 比如 "articles"
        :return: func, 比如 create_article
        """
        return {
            "articles": self.create_article,
            "journals": self.create_journal,
            "gitbooks": self.create_gitbook,
        }[types]

    def create_tag(self, tag_name=None):
        if not tag_name:
            tag_name = self.get_random_string(10)
        return Tag.objects.create(tag_name=tag_name)

    @staticmethod
    def model_map(types):
        """
        对 model 进行映射
        :param types: str(), 比如 "articles"
        :return: model, 比如 Article
        """
        return {
            "articles": Article,
            "journals": Journal,
            "gitbooks": GitBook,
        }[types]


class BasicTest(CreateTestData, TestCase):
    test_file_path = os.path.join(settings.BASE_DIR, "articles", "tests")
    test_markdown_file_path = os.path.join(test_file_path, "markdown_file_for_test.md")
    unfriendly_test_markdown_file_path = os.path.join(test_file_path, "unfriendly_markdown_file_for_test.md")

    article_git_test_md_file_name = "测试笔记-测试用的笔记.md"
    notes_git_path = os.path.join(const.NOTES_PATH_PARENT_DIR, const.NOTES_PATH_NAME)
    article_git_test_md_file_path = os.path.join(notes_git_path, article_git_test_md_file_name)

    gitbook_category_dict = const.GITBOOK_CODES_REPOSITORY
    gitbook_notes_git_path = const.GITBOOK_CODES_PATH

    journal_test_md_file_name = "2017-02-03-任务情况总结测试笔记.md"  # 注意这里不能有空格, 要不然 git 命令就失败了...
    journals_git_path = os.path.join(const.NOTES_PATH_PARENT_DIR, const.JOURNALS_PATH_NAME)
    journal_test_md_file_path = os.path.join(journals_git_path, journal_test_md_file_name)

    @staticmethod
    def create_multiple_articles(article_number=None):
        if not article_number:
            article_number = 3
        for i in range(article_number):
            Article.objects.create(title="test_article_{}".format(i + 1))

    def create_multiple_journals(self, journal_number=None):
        test_date = datetime.datetime.today()

        # 测试 10 篇文章
        for i in range(journal_number):
            self.create_journal(title="test_journal_{}".format(i + 1), date=test_date)
            test_date += datetime.timedelta(days=1)

    def create_markdown_article(self):
        with open(self.test_markdown_file_path, "r") as f:
            data = f.read()
        Article.objects.create(title="test_article_1", content=data)

    def read_test_markdown_file(self, md_file_path=None):
        if not md_file_path:
            md_file_path = self.test_markdown_file_path
        with open(md_file_path, "r") as f:
            data = f.read()
        return data

    def parse_article_git_test_md_file_name(self):
        article = self.article_git_test_md_file_name[:-len(".md")]  # 去掉 .md
        article_category, article_title = article.split("-")  # 分离 "测试笔记-"
        article_content = get_right_content_from_file(self.article_git_test_md_file_path)
        return article, article_title, article_content, article_category

    def parse_journal_git_test_md_file_name(self):
        test_journal_title = self.journal_test_md_file_name[:-len(".md")]  # 去掉 .md
        test_journal_content = get_right_content_from_file(self.journal_test_md_file_path)

        return test_journal_title, test_journal_content

    def create_test_db(self):
        """
        建立 articles、journal、gitbooks 的测试数据
        """
        journal = self.create_journal()
        article = self.create_article(title="test_article", content="test_article")
        gitbooks = self.create_gitbook()

        return article, journal, gitbooks

    @staticmethod
    def create_search(search_content=None, search_choice=None):
        if not search_content:
            search_content = "I HaVe bIg letters"
        if not search_choice:
            search_choice = "all"

        return SearchModel.objects.create(search_content=search_content, search_choice=search_choice)

    @staticmethod
    def display_url_map(types):
        """
        对显示笔记的 URL 进行映射
        :param types: str(), 比如 "articles"
        :return: str, 比如 "/articles/{}/"
        """
        return {
            "articles": article_display_url,
            "journals": journal_display_url,
            "gitbooks": gitbook_display_url,
        }[types]


if __name__ == "__main__":
    pass
