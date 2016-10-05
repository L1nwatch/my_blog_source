#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""

2016.10.03 测试视图函数是否正常
"""
from django.test import TestCase
from django.conf import settings
from articles.models import Article
from articles.views import HOME_PAGE_ARTICLES_NUMBERS

__author__ = '__L1n__w@tch'

TEST_GIT_REPOSITORY = settings.TEST_GIT_REPOSITORY


class HomeViewTest(TestCase):
    def test_use_home_template(self):
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


class DetailViewTest(TestCase):
    def test_use_article_template(self):
        Article.objects.create(title="test_article_1")
        response = self.client.get("/articles/{}/".format(1))
        self.assertTemplateUsed(response, "article.html")


class AboutMeViewTest(TestCase):
    def test_use_about_me_template(self):
        response = self.client.get("/articles/about_me/")
        self.assertTemplateUsed(response, "about_me.html")


class ArchivesViewTest(TestCase):
    def test_use_archives_template(self):
        response = self.client.get("/articles/archives/")
        self.assertTemplateUsed(response, "archives.html")


class SearchTagViewTest(TestCase):
    def test_can_get_same_category(self):
        test_category_name = "test_category"
        article_1 = Article.objects.create(title="article_1", category=test_category_name)
        article_2 = Article.objects.create(title="article_2", category=test_category_name)
        article_3 = Article.objects.create(title="article_3")

        # 查找同一分类下的所有文章
        response = self.client.get("/articles/tag{}/".format(test_category_name))
        self.assertTemplateUsed(response, "tag.html")

        # 不属于这个分类的都不会找到
        self.assertContains(response, article_1.title)
        self.assertContains(response, article_2.title)
        self.assertNotContains(response, article_3.title)


class UpdateNotesViweTest(TestCase):
    def test_can_get_md_from_git(self):
        print(settings.TEST_GIT_REPOSITORY)


if __name__ == "__main__":
    pass
