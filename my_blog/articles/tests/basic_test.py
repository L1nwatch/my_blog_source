#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 作为测试基类

2017.04.03 重构一下创建测试数据的代码, 将其分离出来单独作为一个基类了
"""
import datetime
import os

from django.test import TestCase
from django.conf import settings

from articles.models import Article, SearchModel
from work_journal.models import Journal
from gitbook_notes.models import GitBook
from my_constant import const

__author__ = '__L1n__w@tch'


class BasicTest(TestCase):
    test_file_path = os.path.join(settings.BASE_DIR, "articles", "tests")
    test_markdown_file_path = os.path.join(test_file_path, "markdown_file_for_test.md")
    unfriendly_test_markdown_file_path = os.path.join(test_file_path, "unfriendly_markdown_file_for_test.md")

    git_test_md_file_name = "测试笔记-测试用的笔记.md"
    notes_git_path = os.path.join(const.NOTES_PATH_PARENT_DIR, const.NOTES_PATH_NAME)
    git_test_md_file_path = os.path.join(notes_git_path, git_test_md_file_name)

    @staticmethod
    def create_multiple_articles(article_number=None):
        if not article_number:
            article_number = 3
        for i in range(article_number):
            Article.objects.create(title="test_article_{}".format(i + 1))

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
            title = "title"
        if not content:
            content = "content"
        if not category:
            category = "category"
        return Article.objects.create(title=title, content=content, category=category)

    def parse_git_test_md_file_name(self):
        article = self.git_test_md_file_name[:-len(".md")]  # 去掉 .md
        article_category, article_title = article.split("-")  # 分离 "测试笔记-"
        article_content = get_right_content_from_file(self.git_test_md_file_path)
        return article, article_title, article_content, article_category

    @staticmethod
    def create_journal(title=None, content=None, date=None):
        if not title:
            title = "test_journal"
        if not content:
            content = "test journal"
        if not date:
            date = datetime.datetime.today()

        return Journal.objects.create(title=title, date=date, content=content)

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


if __name__ == "__main__":
    pass
