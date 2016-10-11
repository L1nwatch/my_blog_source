#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""

2016.10.04 更新一下关于首页搜索按钮的测试, 现在要求能够搜索各个文章的标题
2016.10.03 编写功能测试, 第一个编写的功能测试测试首页各个按钮, 包括主页,about 按钮,github 按钮,archive 按钮,email 按钮
"""
from .base import FunctionalTest
from articles.models import Article, Tag
import unittest
from selenium.common.exceptions import NoSuchElementException

__author__ = '__L1n__w@tch'


class TestHomePageButtons(FunctionalTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        super().setUp()
        # Y 访问首页
        self.browser.get(self.server_url)

    def test_home_page_button(self):
        home_page_url = self.browser.current_url
        home_page_source = self.browser.page_source

        # 看到左边第一个按钮, 主页按钮, 点击进去, 没什么反应, 发现自己原来已经在首页了
        home_page_button = self.browser.find_element_by_id("id_home_page")
        home_page_button.click()
        # url 没变化
        self.assertEqual(self.browser.current_url, home_page_url)

        # 点击另一个按钮, about_me 按钮, 发现界面已经变化了, 然后再点击主页按钮, 发现确实可以回到首页
        self.browser.find_element_by_id("id_about_me").click()
        # url 变化了, 页面内容也变化了
        self.assertNotEqual(self.browser.current_url, home_page_url)
        self.assertNotEqual(self.browser.page_source, home_page_source)

    def test_about_me_button(self):
        home_page_source = self.browser.page_source

        # 看到 about_me 按钮, 点击, 发现界面有所变化, 并且显示了作者的相关信息, 特别注意到了座右铭: "Valar Morghulis"
        self.browser.find_element_by_id("id_about_me").click()
        self.assertNotEqual(self.browser.page_source, home_page_source)
        table = self.browser.find_element_by_id("id_information_list")
        rows = table.find_elements_by_tag_name("tr")
        self.assertIn(r"座右铭: Valar Morghulis", [row.text for row in rows])

    def test_github_button(self):
        # 看到 github 按钮, 点击, 发现确实跳转到了一个 github 页面上, 而且 github 页面的用户是 "L1nwatch"
        self.browser.find_element_by_id("id_github").click()
        self.assertIn("github", self.browser.current_url)
        self.assertIn("L1nwatch", self.browser.current_url)

    def test_archive_button(self):
        # 创建测试数据
        self._create_test_db_data()

        # 刷新首页
        self.browser.refresh()
        home_page_source = self.browser.page_source
        home_page_url = self.browser.current_url

        # 看到了归档按钮, 不知道有什么用, 点击看看
        self.browser.find_element_by_id("id_archives").click()

        # 发现 URL 变了
        self.assertNotEqual(self.browser.current_url, home_page_url)

        # 看见页面显示的内容跟首页不一样了
        self.assertNotEqual(self.browser.page_source, home_page_source)

        # 而且不显示文章内容
        with self.assertRaises(NoSuchElementException):
            # 如果找不到会抛出 NoSuchElementException 异常
            self.browser.find_element_by_id("id_article_content")

        # 重新点击首页按钮, 发现首页是会显示文章部分内容的
        self.browser.find_element_by_id("id_home_page").click()
        self.browser.find_element_by_id("id_article_content")

    def test_email_button(self):
        # Y 想联系网站拥有者, 发现了个 email 按钮
        email_button = self.browser.find_element_by_id("id_email")

        # 点击后发现页面跳转了, 而且可以看到 url 中有个 mail to 字母, 后面跟着作者的邮箱: "watch1602@gmail.com"
        # 发现如果使用 click 会使用默认浏览器打开然后就无法测试了, 所以就改用下面这种方法
        self.assertEqual("mailto:watch1602@gmail.com", email_button.get_attribute("href"))


class TestSearchButton(FunctionalTest):
    def setUp(self):
        super().setUp()

        # 创建测试数据
        self._create_test_db_data()

        # Y 访问首页
        self.browser.get(self.server_url)

    def test_can_search_title(self):
        """
        2016.10.04 测试能够搜索各个文章的标题即可
        :return:
        """
        # Y 看到了这个搜索按钮
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
        # Y 看到了搜索按钮
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


if __name__ == "__main__":
    pass
