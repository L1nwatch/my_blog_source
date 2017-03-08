#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.02.18 增加首页搜索的测试
2017.02.11 不断强化搜索功能
2017.02.08 重构, 将原先所有 ArticleForm 改为 BaseSearchForm
2017.01.28 加强了搜索结果显示
2016.10.03 测试视图函数是否正常
"""
import os
import unittest
import shutil
import datetime

from articles.forms import BaseSearchForm, ArticleForm
from articles.models import Article
from articles.views import _parse_markdown_file, get_right_content_from_file, _get_id_from_markdown_html
from articles.templatetags.custom_filter import custom_markdown

from work_journal.models import Journal
from my_constant import const

from django.conf import settings
from django.test import TestCase, override_settings

__author__ = '__L1n__w@tch'


class HomeViewTest(TestCase):
    def test_use_home_template(self):
        """
        测试是否使用了首页的模板
        :return:
        """
        response = self.client.get("/")
        self.assertTemplateUsed(response, "new_home.html")

    def test_only_display_part_articles(self):
        """
        测试是否只显示了部分的文章, 而不是显示所有文章
        :return:
        """
        error_message = "显示了超过 {} 篇文章在首页了".format(const.HOME_PAGE_ARTICLES_NUMBERS)
        for i in range(const.HOME_PAGE_ARTICLES_NUMBERS + 10):
            Article.objects.create(title="test_article_{}".format(i + 1))

        response = self.client.get("/")
        counts = 0
        for article in Article.objects.all():
            article_url = "/articles/{}/".format(article.id)
            if article_url.encode("utf8") in response.content:
                counts += 1
            self.assertFalse(counts > const.HOME_PAGE_ARTICLES_NUMBERS, error_message)

    def test_home_page_uses_article_form(self):
        response = self.client.get("/")
        # 使用 assertIsInstance 确认视图使用的是正确的表单类
        self.assertIsInstance(response.context["form"], BaseSearchForm)
        self.assertContains(response, 'name="title"')


class ArticleDisplayViewTest(TestCase):
    unique_url = "/articles/{}/"

    def setUp(self):
        self._create_markdown_article()

    @staticmethod
    def _create_markdown_article():
        with open(os.path.join(settings.BASE_DIR, "markdown_file_for_test.md"), "r") as f:
            data = f.read()
        Article.objects.create(title="test_article_1", content=data)

    def test_use_article_template(self):
        response = self.client.get(self.unique_url.format(1))
        self.assertTemplateUsed(response, "article.html")

        # 测试是否有将 form 传递给模板
        self.assertIsInstance(response.context["form"], ArticleForm)

    def test_markdown_parse(self):
        """
        测试 markdown 解析成树效果
        :return:
        """
        with open(os.path.join(settings.BASE_DIR, "markdown_file_for_test.md"), "r") as f:
            data = f.read()

        my_parse_result = _parse_markdown_file(data)

        self.assertNotEqual(my_parse_result, None)
        self.assertEqual(my_parse_result[0].title, "一级标题")
        self.assertEqual(my_parse_result[0].child[0].title, "二级标题")
        self.assertEqual(my_parse_result[0].child[0].child[0].title, "三级标题 1")
        self.assertEqual(my_parse_result[0].child[0].child[1].title, "三级标题 2")

    def test_markdown_tree_display(self):
        """
        测试解析后的 markdown 树是否显示在界面中
        """
        response = self.client.get(self.unique_url.format(1))
        self.assertTrue(response.content.decode("utf8").count("一级标题") >= 3)
        self.assertTrue(response.content.decode("utf8").count("二级标题") >= 3)
        self.assertTrue(response.content.decode("utf8").count("三级标题 1") >= 3)
        self.assertTrue(response.content.decode("utf8").count("三级标题 2") >= 2)

    def test_markdown_tree_href(self):
        """
        解析后的 markdown 树应该有对应的 href 属性才对
        """
        response = self.client.get(self.unique_url.format(1))

        self.assertIn('href="#_1"', response.content.decode("utf8"))  # 一级标题
        self.assertIn('href="#_2"', response.content.decode("utf8"))  # 二级标题
        self.assertIn('href="#1"', response.content.decode("utf8"))  # 三级标题 1
        self.assertIn('href="#2"', response.content.decode("utf8"))  # 三级标题 2

    def test_get_id_right(self):
        """
        测试获取 id 的正则是否写对了
        """
        with open(os.path.join(settings.BASE_DIR, "markdown_file_for_test.md"), "r") as f:
            data = f.read()

        markdown_html = custom_markdown(data)

        self.assertEqual(_get_id_from_markdown_html(markdown_html, "一级标题"), "_1")
        self.assertEqual(_get_id_from_markdown_html(markdown_html, "二级标题"), "_2")
        self.assertEqual(_get_id_from_markdown_html(markdown_html, "三级标题 1"), "1")
        self.assertEqual(_get_id_from_markdown_html(markdown_html, "三级标题 2"), "2")
        self.assertEqual(_get_id_from_markdown_html(markdown_html, "四级标题"), "_3")


class AboutMeViewTest(TestCase):
    unique_url = "/articles/about_me/"

    def test_use_about_me_template(self):
        response = self.client.get(self.unique_url)
        self.assertTemplateUsed(response, "about_me.html")

    def test_view_passes_form_to_template(self):
        """
        测试是否有将 form 传递给模板
        """
        response = self.client.get(self.unique_url)
        self.assertIsInstance(response.context["form"], BaseSearchForm)


class ArchivesViewTest(TestCase):
    unique_url = "/articles/archives/"

    def test_use_archives_template(self):
        response = self.client.get(self.unique_url)
        self.assertTemplateUsed(response, "archives.html")

    def test_view_passes_form_to_template(self):
        """
        测试是否有将 form 传递给模板
        """
        response = self.client.get(self.unique_url)
        self.assertIsInstance(response.context["form"], ArticleForm)


class SearchTagViewTest(TestCase):
    unique_url = "/articles/tag{}/"

    def test_can_get_same_category(self):
        test_category_name = "test_category"
        article_1 = Article.objects.create(title="article_1", category=test_category_name)
        article_2 = Article.objects.create(title="article_2", category=test_category_name)
        article_3 = Article.objects.create(title="article_3")

        # 查找同一分类下的所有文章
        response = self.client.get(self.unique_url.format(test_category_name))
        self.assertTemplateUsed(response, "tag.html")

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


@override_settings(UPDATE_TIME_LIMIT=0.1)
@unittest.skipUnless(const.SLOW_CONNECT_DEBUG, "[*] 用户选择忽略部分测试")
class UpdateNotesViewTest(TestCase):
    unique_url = "/articles/update_notes/"
    test_md_file_name = "测试笔记-测试用的笔记.md"

    notes_git_path = os.path.join(const.NOTES_PATH_PARENT_DIR, const.NOTES_PATH_NAME)
    test_md_file_path = os.path.join(notes_git_path, test_md_file_name)

    def __update_test_md_file_and_git_push(self, test_content):
        """
        更新测试文件并将内容上传到仓库中
        :return:
        """
        with open(self.test_md_file_path, "w") as f:
            f.write(test_content)
        command = "cd {} && git add -A && git commit -m '测试开始' && git push".format(self.notes_git_path)
        os.system(command)

    def setUp(self):
        """
        主要是在测试之前备份笔记文件
        :return:
        """
        # 确保已经进行过 git 操作
        if not os.path.exists(os.path.join(self.notes_git_path, ".git")):
            self.client.get(self.unique_url)

        # 创建测试文件并上传到 git 仓库中
        self.old_file_content = "# 测试1234"
        self.__update_test_md_file_and_git_push(self.old_file_content)

    def tearDown(self):
        """
        主要是在测试结束之后恢复笔记文件
        :return:
        """
        # 删除测试文件
        command = "cd {}" \
                  " && rm {}" \
                  " && git add -A" \
                  " && git commit -m '测试完毕'" \
                  " && git push".format(self.notes_git_path, self.test_md_file_name)
        os.system(command)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        # 删除整个 notes 测试文件夹
        shutil.rmtree(const.NOTES_GIT_PATH)

    def test_can_get_md_from_git(self):
        self.client.get(self.unique_url)

        if not os.path.exists(self.test_md_file_path):
            self.fail("从 git 上获取文件失败了")

    def test_can_sync_md_from_git(self):
        """
        确保获取到的是 git 上的最新版本
        :return:
        """
        # 更改文件夹中的测试文件, git 提交到仓库上
        test_content = "# test1234"
        self.__update_test_md_file_and_git_push(test_content)

        # 恢复旧的测试文件
        with open(self.test_md_file_path, "w") as f:
            f.write(self.old_file_content)

        # 再次执行该视图函数, 发现文件夹里的旧测试文件已经变成新的测试文件了
        self.client.get(self.unique_url)
        data = get_right_content_from_file(self.test_md_file_path)
        self.assertEqual(data, test_content, "更新测试文件失败")

    def test_create_notes_from_md(self):
        # 每个 md 笔记的文件名类似于: "测试笔记-测试用的笔记.md"
        test_article = self.test_md_file_name.rstrip(".md")  # 去掉 .md
        test_article_title = test_article.split("-")[1]  # 去掉 "测试笔记-"
        test_article_content = get_right_content_from_file(self.test_md_file_path)
        article = None

        # 一开始没有这篇文章
        with self.assertRaises(Article.DoesNotExist):
            article = Article.objects.get(title=test_article_title)
        self.assertEqual(article, None, "一开始不应该有这篇文章的")

        # 执行完该视图函数之后就有了
        self.client.get(self.unique_url)
        try:
            article = Article.objects.get(title=test_article_title)
            self.assertTrue(article is not None, "没有成功更新数据库啊")
            self.assertEqual(article.content, test_article_content, "文件内容不对啊")
        except Article.DoesNotExist:
            self.fail("没有成功更新数据库啊")

    def test_update_notes_from_md(self):
        # 每个 md 笔记的文件名类似于: "测试笔记-测试用的笔记.md"
        test_article = self.test_md_file_name.rstrip(".md")  # 去掉 .md
        test_article_category, test_article_title = test_article.split("-")  # 去掉 "测试笔记-"
        Article.objects.create(title=test_article_title, category="old_category", content="old content")

        # 文章进行了更新
        test_content = "# test_hello"
        self.__update_test_md_file_and_git_push(test_content)

        # 再次执行该视图函数, 发现数据库也跟着更新了
        self.client.get(self.unique_url)
        latest_article = Article.objects.get(title=test_article_title)
        self.assertEqual(latest_article.content, test_content, "数据库中依然是老文章的内容")
        self.assertEqual(latest_article.category, test_article_category, "数据库中依然是老文章的分类")

    def test_update_time_when_update_notes(self):
        # 旧的一份笔记
        test_article = self.test_md_file_name.rstrip(".md")  # 去掉 .md
        test_article_category, test_article_title = test_article.split("-")  # 去掉 "测试笔记-"
        old_article = Article.objects.create(title=test_article_title, category="old_category", content="old content")

        # 文章进行了跟新
        test_content = "# test_hello"
        self.__update_test_md_file_and_git_push(test_content)

        # 再次执行该视图函数, 发现数据库也跟着更新了, 尤其是更新时间刷新了
        self.client.get(self.unique_url)
        latest_article = Article.objects.get(title=test_article_title)
        self.assertNotEqual(old_article.update_time, latest_article.update_time)

    def test_view_passes_form_to_template(self):
        """
        测试是否有将 form 传递给模板
        """
        response = self.client.get(self.unique_url)
        self.assertIsInstance(response.context["form"], BaseSearchForm)

    def test_delete_notes_from_md(self):
        """
        原先在数据库中已经存在某个笔记, 但是最新版本的 git 仓库中并没有这个笔记, 那么从数据库中删除掉
        :return:
        """
        should_not_exist_note = Article.objects.create(title="不应该存在的笔记", category="测试笔记")

        # 确认仓库中没有这个笔记
        not_exist_note_full_name = "{}-{}.md".format(should_not_exist_note.category, should_not_exist_note.title)
        self.assertNotIn(not_exist_note_full_name, os.listdir(self.notes_git_path))

        # 执行视图函数
        self.client.get(self.unique_url)

        # 发现数据库中已经不存在该笔记了
        with self.assertRaises(Article.DoesNotExist):
            Article.objects.get(title=should_not_exist_note.title)


class ArticlesSearchViewTest(TestCase):
    unique_url = "/search/search_type=articles"

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post(self.unique_url, data={"title": ""})
        # 此时应该是返回到首页了
        self.assertIsInstance(response.context["form"], BaseSearchForm)

    def test_for_valid_input_passes_form_to_template(self):
        response = self.client.post(self.unique_url, data={"title": "不应该有这篇文章的"})
        self.assertIsInstance(response.context["form"], ArticleForm)

    def test_form_input_not_exist_title(self):
        form = ArticleForm(data={"title": ""})
        self.assertEqual(form.errors["title"], [const.EMPTY_ARTICLE_ERROR])

    def test_view_passes_form_to_template(self):
        """
        测试是否有将 form 传递给模板
        """
        response = self.client.get(self.unique_url)
        # GET 请求, 到首页, 应该是 BaseForm
        self.assertIsInstance(response.context["form"], BaseSearchForm)

    def test_valid_input_will_get_response_using_right_template(self):
        test_article = Article.objects.create(title="test_article")
        response = self.client.post(self.unique_url, data={"title": test_article.title})
        self.assertTemplateUsed(response, "search_result.html")

    def test_id_article_exist(self):
        """
        搜索存在的文章, 显示出来的界面中每篇文章标题应该有 const.ID_SEARCH_RESULT_TITLE 这个属性
        :return:
        """
        test_article_title = "test_for_search_button"
        Article.objects.create(title=test_article_title)

        response = self.client.post(self.unique_url, data={"title": test_article_title})
        self.assertContains(response, const.ID_SEARCH_RESULT_TITLE)

    def test_can_search_content(self):
        """
        测试搜索文章的时候会去搜索文章内容
        :return:
        """
        test_article = Article.objects.create(title="test_title_文章", content="test_content")
        response = self.client.post(self.unique_url, data={"title": test_article.content})
        self.assertContains(response, test_article.title)

    def test_search_content_without_case(self):
        """
        测试搜索文章内容的时候会忽略大小写
        :return:
        """
        test_article = Article.objects.create(title="test_title_文章", content="test_content")
        response = self.client.post(self.unique_url, data={"title": "TeSt_ConTeNt"})
        self.assertContains(response, test_article.title)

    def test_can_search_content_and_title(self):
        """
        测试搜索出来的内容会从文章以及标题去查找
        :return:
        """
        test_article = Article.objects.create(title="test_title_文章", content="test_content")
        # 从标题中查找
        response = self.client.post(self.unique_url, data={"title": "title"})
        self.assertContains(response, test_article.title)

        # 从内容中查找
        response = self.client.post(self.unique_url, data={"title": "content"})
        self.assertContains(response, test_article.title)

    def test_search_multiple_words(self):
        """
        测试能够同时搜索多个关键词
        :return:
        """
        test_article = Article.objects.create(title="test_title_文章", content="test content content2")
        # 仅存在其中一个关键词
        response = self.client.post(self.unique_url, data={"title": "content3 test"})
        self.assertNotContains(response, test_article.title)

        # 两个关键词都存在
        response = self.client.post(self.unique_url, data={"title": "content2 test"})
        self.assertContains(response, test_article.title)

    def test_search_one_word_can_show_content_and_title(self):
        """
        测试只搜索一个关键词的时候, 能找到对应的内容及标题
        """
        test_article = Article.objects.create(title="test_title_article", content="aaa\nbbb\nccc\nddd\n")

        # 关键词在内容中, 搜索 bbb
        response = self.client.post(self.unique_url, data={"title": "bBb"})  # 搜索要支持大小写

        # 对应文章的标题存在
        self.assertContains(response, test_article.title)
        # 对应行的内容存在
        self.assertContains(response, "bBb")
        # 没搜索的行不应该存在
        self.assertNotContains(response, "ccc")
        # 信息也不应该是提示信息
        self.assertNotContains(response, const.KEYWORD_IN_TITLE)

        # 关键词在标题中, 搜索 article
        response = self.client.post(self.unique_url, data={"title": "arTicle"})
        # 对应文章的标题存在
        self.assertContains(response, test_article.title)
        # 对应行的内容存在, 行内容为常量, 类似于 "关键词仅出现标题中" 等的提示信息
        self.assertContains(response, const.KEYWORD_IN_TITLE)

        # 关键词不在标题也不在内容, 搜索 bbbb
        response = self.client.post(self.unique_url, data={"title": "bbbb"})
        # 对应文章的标题不存在
        self.assertNotContains(response, test_article.title)
        # 显示文章找不到的提示信息
        self.assertContains(response, const.EMPTY_ARTICLE_ERROR)

    def test_search_multiple_words_can_show_contents_and_title(self):
        """
        测试搜索多个关键词的时候, 每个关键词对应的行都显示了出来
        """
        test_article = Article.objects.create(title="test_title_article", content="aaa\nbbb\nccc\nddd\n")

        # 关键词在内容中, 搜索 ccc 和 aaa
        response = self.client.post(self.unique_url, data={"title": "ccc aaa"})

        # 对应文章的标题存在
        self.assertContains(response, test_article.title)
        # 对应行的内容存在
        self.assertContains(response, "ccc")
        self.assertContains(response, "aaa")
        # 没搜索的行不应该存在
        self.assertNotContains(response, "bbb")

        # 关键词在标题和内容中, 搜索 article 和 bbb
        response = self.client.post(self.unique_url, data={"title": "article bbb"})
        # 对应文章的标题存在
        self.assertContains(response, test_article.title)
        # 对应行的内容存在, 行内容为常量, 类似于 "关键词仅出现标题中" 等的提示信息
        self.assertContains(response, "bbb")
        self.assertNotContains(response, const.KEYWORD_IN_TITLE)

    def test_search_multiple_articles(self):
        """
        没想到自己手测才发现这个错误, 就是只有第一个搜索结果是正确的, 其他几篇文章的搜索结果都是错误的
        """
        test_article = Article.objects.create(title="test_title_article", content="aaa\nbbb\nccc\nddd\n")
        test_article2 = Article.objects.create(title="test_title_article2", content="eee\nbbb\nfff\nddd\n")

        # 关键词在内容中, 搜索 bbb
        response = self.client.post(self.unique_url, data={"title": "bbb"})

        # 两篇文章都存在
        self.assertContains(response, test_article.title)
        self.assertContains(response, test_article2.title)

        # bbb 至少出现了 2 次, 比如搜索框里还有一次
        self.assertTrue(response.content.decode("utf8").count("bbb") >= 2)

    def test_search_result_with_right_href(self):
        """
        测试搜索结果显示了正确的 href
        """
        test_article = Article.objects.create(title="test_title_article", content="aaa\nbbb\nccc\nddd\n")

        # 关键词在内容中, 搜索 bbb
        response = self.client.post(self.unique_url, data={"title": "bbb"})

        # 能搜索到文章
        self.assertContains(response, test_article.title)

        # 标题 href 正确
        self.assertContains(response, "/articles/{}/".format(test_article.id))

    def test_search_multiple_words_without_case(self):
        """
        功能测试发现的, 搜索多个关键词的时候, 存在大小写问题
        """
        test_article = Article.objects.create(title="test_title_article", content="aaa\nbBb\ncCc\nddd\n")

        # 关键词在内容中, 搜索 bbb
        response = self.client.post(self.unique_url, data={"title": "ddd Bbb"})

        # 能搜索到文章
        self.assertContains(response, test_article.title)


class BaseSearchViewTest(TestCase):
    unique_url = "/search/search_type=all"

    def test_for_valid_input_passes_form_to_template(self):
        """
        测试 form 使用正确
        """
        response = self.client.post(self.unique_url, data={"title": "不应该有这篇文章的"})
        self.assertIsInstance(response.context["form"], BaseSearchForm)

    def test_can_search_articles_and_journals(self):
        # 创建测试数据
        journal = Journal.objects.create(title="test_journal", date=datetime.datetime.today(), content="test journal")
        article = Article.objects.create(title="test_article", content="test_article")

        # 测试搜索
        response = self.client.post(self.unique_url, data={"title": "test"})

        # 能搜索到文章
        self.assertContains(response, article.title)

        # 能搜索到日记
        self.assertContains(response, journal.title)

    def test_search_not_exist_keyword(self):
        response = self.client.post(self.unique_url, data={"title": "随便输入的一点什么东西"})

        self.assertContains(response, const.EMPTY_ARTICLE_ERROR)

    def test_second_search_still_same_url(self):
        """
        测试搜索界面再次搜索的时候依旧是 all 搜索
        """
        response = self.client.post(self.unique_url, data={"title": "随便输入的一点什么东西"})

        self.assertNotContains(response, ArticlesSearchViewTest.unique_url)
        self.assertContains(response, self.unique_url)


if __name__ == "__main__":
    pass
