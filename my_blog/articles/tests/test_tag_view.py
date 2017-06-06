#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 测试有关 category/tag 的视图函数

2017.06.06 将有关 category/tag 视图函数的测试都抽出来放到了这个脚本之中
"""
# 自己的模块
from common_module.tests.basic_test import BasicTest, category_search_url, tag_search_url
from articles.forms import ArticleForm
from articles.models import Tag

__author__ = '__L1n__w@tch'


class SearchCategoryViewTest(BasicTest):
    unique_url = category_search_url

    def test_can_get_same_category(self):
        test_category_name = "test_category"
        article_1 = self.create_article(title="article_1", category=test_category_name)
        article_2 = self.create_article(title="article_2", category=test_category_name)
        article_3 = self.create_article(title="article_3")

        # 查找同一分类下的所有文章
        response = self.client.get(self.unique_url.format(test_category_name))
        self.assertTemplateUsed(response, "tag_category.html")

        # 不属于这个分类的都不会找到
        self.assertContains(response, article_1.title)
        self.assertContains(response, article_2.title)
        self.assertNotContains(response, article_3.title)

    def test_view_passes_form_to_template(self):
        """
        测试是否有将 form 传递给模板
        """
        response = self.client.get(self.unique_url.format("just_a_test"))
        self.assertIsInstance(response.context["form"], ArticleForm)


class SearchTagViewTest(BasicTest):
    unique_url = tag_search_url

    def test_can_get_same_tag(self):
        """
        测试在搜索 tag 时, 相同 tag 的文章都会被搜索出来
        """
        test_tag_name = "test_tag"
        test_tag = Tag.objects.get_or_create(tag_name=test_tag_name)

        article_1 = self.create_article(article_tag=test_tag)
        article_2 = self.create_article(article_tag=test_tag)
        article_3 = self.create_article()

        # 查找同一分类下的所有文章
        response = self.client.get(self.unique_url.format(test_tag_name))
        self.assertTemplateUsed(response, "tag_category.html")

        # 不属于这个分类的都不会找到
        self.assertContains(response, article_1.title)
        self.assertContains(response, article_2.title)
        self.assertNotContains(response, article_3.title)


if __name__ == "__main__":
    pass
