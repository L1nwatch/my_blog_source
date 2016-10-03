#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""

2016.10.03 测试视图函数是否正常
"""
from django.test import TestCase
from articles.models import Article
from articles.views import HOME_PAGE_ARTICLES_NUMBERS

__author__ = '__L1n__w@tch'


class HomeViewTest(TestCase):
    def test_use_home_templates(self):
        """
        测试是否使用了首页的模板
        :return:
        """
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_only_display_part_articles(self):
        """
        测试是否只显示了部分的文章, 而不是显示所有文章
        :return:
        """
        error_message = "显示了超过 {} 篇文章在首页了".format(HOME_PAGE_ARTICLES_NUMBERS)
        for i in range(HOME_PAGE_ARTICLES_NUMBERS + 10):
            Article.objects.create(title="test_article_{}".format(i + 1))

        response = self.client.get("/")
        counts = 0
        for article in Article.objects.all():
            article_url = "/articles/{}/".format(article.id)
            if article_url.encode("utf8") in response.content:
                counts += 1
            self.assertFalse(counts > HOME_PAGE_ARTICLES_NUMBERS, error_message)


if __name__ == "__main__":
    pass
