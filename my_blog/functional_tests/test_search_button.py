#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.01.27 添加搜索时显示对应内容的测试相关代码
2016.10.29 将搜索按钮的测试分离出来, 成为一个单独的测试文件
2016.10.04 更新一下关于首页搜索按钮的测试, 现在要求能够搜索各个文章的标题
"""
from .base import FunctionalTest
from articles.models import Article

__author__ = '__L1n__w@tch'


class TestSearchButton(FunctionalTest):
    def setUp(self):
        super().setUp()

        # 创建测试数据
        self._create_test_db_data()

    def test_can_search_title(self):
        """
        2016.10.04 测试能够搜索各个文章的标题即可
        :return:
        """
        # Y 打开首页, 看到了搜索按钮
        self.browser.get(self.server_url)
        search_button = self.browser.find_element_by_id("id_search")

        # 看着首页右边已经存在的文章, 随便打了一个进去, 然后按下回车键
        newest_article = Article.objects.first()
        search_button.send_keys(newest_article.title + "\n")

        # 发现确实能够搜索出对应的文章出来
        self.assertIn(newest_article.title, self.browser.page_source)

        # Y 想试试如果搜索一篇不存在的文章会怎样, 就随便打了一串字符, 尝试进行搜索
        search_button = self.browser.find_element_by_id("id_search")
        search_button.send_keys("不应该有这篇文章的存在\n")

        # 发现搜索结果为: 没有相关文章题目
        self.assertIn("没有相关文章题目", self.browser.page_source)

    def test_can_search_content(self):
        """
        2016.10.11 测试能够搜索文章内容
        :return:
        """
        # Y 打开首页, 看到了搜索按钮
        self.browser.get(self.server_url)
        search_button = self.browser.find_element_by_id("id_search")

        # Y 记得以前看过的某篇文章中有 time.sleep 方法的示例, 但是不记得文章标题了, 于是搜索这个关键词
        search_button.send_keys("time.sleep\n")

        # Y 发现搜出来了文章, 随便打开一篇文章, 可以看到确实是有 time.sleep 的存在
        articles_after_search = self.browser.find_element_by_id("id_article_title")
        articles_after_search.click()
        self.assertIn("time.sleep", self.browser.find_element_by_tag_name('body').text)

        # Y 想知道这个搜索功能是否类似于 google 搜索, 即可以用空格来区分多个关键词然后进行搜索
        search_button = self.browser.find_element_by_id("id_search")

        # Y 搜索了这么一个关键词: and I, 发现确实搜出来结果了, 而且随便打开一片文章里面可以找到 and 和 I, 而且不是连在一起的
        search_button.send_keys("and I\n")
        articles_after_search = self.browser.find_element_by_id("id_article_title")
        articles_after_search.click()
        body_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn("and", body_text)
        self.assertIn("I", body_text)
        self.assertNotIn("and I", body_text)

        # Y 尝试随便输入一些东西, 看是不是能搜出什么
        search_button = self.browser.find_element_by_id("id_search")
        search_button.send_keys("随便输入了一些什么啊肯定是搜索不到的\n")

        # 果然关键词打得太随意了, 啥都没有啊
        articles_after_search = self.browser.find_elements_by_id("id_article_title")
        self.assertTrue(len(articles_after_search) == 0, "居然找到文章了?!")

    def test_search_result_display(self):
        """
        测试搜索的结果, 应该显示对应的文章及对应到的搜索内容
        """
        # Y 打开首页, 看到了搜索按钮
        self.browser.get(self.server_url)
        search_button = self.browser.find_element_by_id("id_search")

        # Y 知道文章 <article_with_markdown> 有这么一个关键字 <markdown1>, 所在行内容为 <* test markdown1>
        # 于是 Y 搜索 markdown1, 看是否显示这篇文章及结果出来
        search_button.send_keys("markdown1\n")

        # 搜索结果出来了, Y 看到了自己搜索的关键词
        search_keyword = self.browser.find_element_by_id("id_search").get_attribute("value")
        self.assertEqual(search_keyword, "markdown1")

        # Y 查看搜索结果, 发现其找到对应文章了
        search_result = self.browser.find_element_by_tag_name("body").text
        self.assertIn("article_with_markdown", search_result)

        # 显示对应搜索结果
        self.assertIn("test markdown1", search_result)


if __name__ == "__main__":
    pass
