#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 作为测试基类

2017.04.03 重构一下创建测试数据的代码, 将其分离出来单独作为一个基类了
"""
import datetime
import os
import string
import random

from django.test import TestCase
from django.conf import settings

from articles.models import Article, SearchModel
from articles.views import get_right_content_from_file
from work_journal.models import Journal
from gitbook_notes.models import GitBook
from code_collect.models import CodeCollect
from my_constant import const

__author__ = '__L1n__w@tch'


class BasicTest(TestCase):
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

    def read_test_markdown_file(self):
        with open(self.test_markdown_file_path, "r") as f:
            data = f.read()
        return data

    @staticmethod
    def create_article(title=None, content=None, category=None):
        if not title:
            title = "".join([random.choice(string.ascii_letters) for j in range(10)])
        if not content:
            content = "content"
        if not category:
            category = "category"
        return Article.objects.create(title=title, content=content, category=category)

    def parse_article_git_test_md_file_name(self):
        article = self.article_git_test_md_file_name[:-len(".md")]  # 去掉 .md
        article_category, article_title = article.split("-")  # 分离 "测试笔记-"
        article_content = get_right_content_from_file(self.article_git_test_md_file_path)
        return article, article_title, article_content, article_category

    def parse_journal_git_test_md_file_name(self):
        test_journal_title = self.journal_test_md_file_name[:-len(".md")]  # 去掉 .md
        test_journal_content = get_right_content_from_file(self.journal_test_md_file_path)

        return test_journal_title, test_journal_content

    @staticmethod
    def create_journal(title=None, content=None, date=None, category=None):
        if not title:
            title = "".join([random.choice(string.ascii_letters) for j in range(10)])
        if not content:
            content = "test journal"
        if not date:
            date = datetime.datetime.today()
        if not category:
            category = "category"

        return Journal.objects.create(title=title, date=date, content=content, category=category)

    @staticmethod
    def create_gitbook(book_name=None, href=None, md_file_name=None, title=None, content=None):
        if not book_name:
            book_name = "test_book_name"
        if not href:
            href = "http://{}/{}.html".format("test_book_name", "test")
        if not md_file_name:
            md_file_name = "test.md"
        if not title:
            title = "test_book_name/test"
        if not content:
            content = "test content"

        gitbook = GitBook.objects.create(
            book_name=book_name,
            href=href,
            md_file_name=md_file_name,
            title=title,
            content=content,
        )

        return gitbook

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

    def create_code(self, note=None, code_type=None):
        if not code_type:
            code_type = "Others"
        if not note:
            note = self.create_article()
        return CodeCollect.objects.create(code_type=code_type, note=note)


if __name__ == "__main__":
    pass
