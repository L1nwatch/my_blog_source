#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 测试有关 Article 归档页的一切

2017.06.15 由于统一了 category 搜索的界面, 对应的测试也得更改, 话说原本由于 PyCharm 无法识别该测试失败, 现在换了一种可以识别的方式
2017.06.06 将所有有关 Archive 都合并到了这个脚本之中, 另外补充有关 Tag 搜索的测试
"""
# 标准库
import datetime
from selenium.common.exceptions import NoSuchElementException

# 自己的模块
from .base import FunctionalTest
from articles.models import Article, Tag

__author__ = '__L1n__w@tch'


class TestHomeArchiveButton(FunctionalTest):
    def test_use_home_archive_button(self):
        """
        测试从首页点击 archive 按钮
        """
        # 创建测试数据
        self.create_articles_test_db_data()

        # 访问首页
        self.browser.get(self.server_url)
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


class TestArchiveDisplay(FunctionalTest):
    """
    文章归档页的相关显示测试
    """

    def setUp(self):
        super().setUp()
        self.create_articles_test_db_data()
        self.test_time = datetime.datetime.now()
        self.test_url = "{host}/{path}".format(host=self.server_url, path="articles/archives/")

        # Y 访问归档页
        self.browser.get(self.test_url)

    def test_has_article_create_time(self):
        # 发现存在创建时间的字样, 而且能看到格式是: "Y 年 m 月 d 号 H 时"
        self.browser.find_element_by_id("id_create_time")
        create_time_label_content = ("Create: {} 年 {} 月 {} 号 {} 时"
                                     .format(self.test_time.year, str(self.test_time.month).zfill(2),
                                             str(self.test_time.day).zfill(2), str(self.test_time.hour).zfill(2)))
        self.assertIn(create_time_label_content, self.browser.page_source)

    def test_has_article_update_time(self):
        # 发现存在更新时间的字样, 而且能看到格式是: "Y 年 m 月 d 号 H 时"
        self.browser.find_element_by_id("id_update_time")
        update_time_label_content = ("Update: {} 年 {} 月 {} 号 {} 时"
                                     .format(self.test_time.year, str(self.test_time.month).zfill(2),
                                             str(self.test_time.day).zfill(2), str(self.test_time.hour).zfill(2)))
        self.assertIn(update_time_label_content, self.browser.page_source)

    def test_tag_html_has_right_time(self):
        """
        测试 tag.html 显示的时间是正确的
        """
        # 发现分类包含个超链接, 点击进去看看
        self.browser.find_element_by_id("id_category").click()

        # 出现了一个新页面, 页面上显示了每篇文章的发布时间
        publish_time_label_content = ("Create: {} 年 {} 月 {} 号 {} 时"
                                      .format(self.test_time.year, str(self.test_time.month).zfill(2),
                                              str(self.test_time.day).zfill(2), str(self.test_time.hour).zfill(2)))
        self.assertTrue(publish_time_label_content in self.browser.page_source)

    def test_display_article_tag(self):
        """
        测试会显示对应文章的 tag 信息
        """
        # 创建测试用的带 tag 的文章
        test_tag = self.create_tag("test_tag")
        test_tag2 = self.create_tag("test_tag2")
        self.create_article(article_tag=(test_tag, test_tag2))

        # 重新访问归档页
        self.browser.get(self.test_url)

        # 发现 2 个 tag 都出现在了归档页中
        self.assertIn(test_tag.tag_name, self.browser.page_source)
        self.assertIn(test_tag2.tag_name, self.browser.page_source)

    def test_tag_can_search(self):
        """
        测试归档页可以通过 tag 进行 tag 搜索, 得到相同 tag 的所有文章
        """
        # Y 打算找一下所有有关 Others 这个 Tag 的文章
        test_tag_name = "Others"
        test_tag = Tag.objects.get(tag_name=test_tag_name)
        archive_url = self.browser.current_url

        tags = self.browser.find_elements_by_id("id_tags")
        # Y 发现 Others 这个 tag 了, 于是点击一下, 看是否能显示出所有包含 Others 这个 Tag 的文章
        for each_tag in tags:
            if each_tag.text == test_tag_name:
                each_tag.click()
                break

        # Y 发现 URL 变化了
        self.assertNotEqual(archive_url, self.browser.current_url)

        # Y 知道总共有 x 篇文章包含有 Others 这个 Tag, 而且界面上刚好就显示了 x 篇文章
        test_articles = Article.objects.filter(tag=test_tag)
        all_display_articles = self.browser.find_elements_by_id("id_article_title")
        self.assertEqual(len(all_display_articles), len(test_articles))

        # Y 一一对应标题, 发现所有包含 Others Tag 的文章都显示在了界面上
        for each_article in test_articles:
            self.assertTrue(any(
                [each_article.title == x.text for x in all_display_articles]
            ))


if __name__ == "__main__":
    pass
