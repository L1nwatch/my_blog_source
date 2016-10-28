#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2016.10.28 将原来的时间改为创建时间, 另外新增一个更新时间的字段, 所以需要进行 model 测试
"""
from django.test import TestCase
from articles.models import Article

__author__ = '__L1n__w@tch'


class ArticleModelTest(TestCase):
    def test_has_create_time_and_update_time(self):
        new_article = Article.objects.create(title="test_article_1", content="test_article_content_1")
        self.assertNotEqual(new_article.create_time, None)
        self.assertNotEqual(new_article.update_time, None)

    def test_create_time_equal_to_update_time_when_create_new_article(self):
        """
        新建一篇文章时, 文章的创建时间和更新时间应该是一样的
        :return:
        """
        new_article = Article.objects.create(title="test_article_1", content="test_article_content_1")
        create_time = "{}/{}/{}/{}".format(new_article.create_time.year, new_article.create_time.month,
                                           new_article.create_time.day, new_article.create_time.hour)
        update_time = "{}/{}/{}/{}".format(new_article.update_time.year, new_article.update_time.month,
                                           new_article.update_time.day, new_article.update_time.hour)
        self.assertEqual(create_time, update_time)


if __name__ == "__main__":
    pass
