#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""

2017.06.16 新增搜索结果显示 GitBook Tag 的相关测试
2017.06.07 补充搜索界面中对 Tag 进行搜索的测试
2017.06.04 重构基类测试, 修改对应代码 + 添加有关搜索结果页面显示 Tag 的测试代码
2017.05.21 新增两个关于搜索结果按照点击次数排序的测试
2017.05.21 重构一下, 把所有测试放到同一个类中不好看
2017.04.30 重新定义搜索结果中 GitBook title 的样式, 另外重构一下代码
2017.03.31 手动调试发现搜索 code 时进入日记有问题, 补充对应测试代码
2017.03.30 补充更新操作, 要不然没法进行 Code 搜索
2017.03.29 新增有关 Code APP 的功能测试代码
2017.03.26 增加特殊字符输入的搜索测试
2017.03.23 增加有关搜索结果按关键词出现次数排序的相关测试代码
2017.03.15 首页添加搜索选项, 于是编写对应的测试代码
2017.03.09 添加搜索结果显示行数的功能测试
2017.03.05 添加 gitbook 的测试代码
2017.02.21 手动使用过程中发现两个毛病, 补充一下测试代码
2017.02.18 添加测试, 要求首页既能搜索文章又能搜索日记
2017.01.27 添加搜索时显示对应内容的测试相关代码
2016.10.29 将搜索按钮的测试分离出来, 成为一个单独的测试文件
2016.10.04 更新一下关于首页搜索按钮的测试, 现在要求能够搜索各个文章的标题
"""
# 标准库
from selenium.common.exceptions import NoSuchElementException

import datetime

# 自己的模块
from .base import FunctionalTest
from articles.models import Article, Tag
from work_journal.models import Journal
from code_collect.views import code_collect
import my_constant as const

__author__ = '__L1n__w@tch'


class BasicSearch(FunctionalTest):
    def do_choose_search(self, pointed_choice, search_content):
        """
        从首页选择某个下拉菜单后进行对应的搜索
        :param pointed_choice: str(), 要选择哪个选项? 比如 "GitBooks"
        :param search_content: str(), 要搜索的内容, 比如 "test"
        :return: None
        """
        # Y 打开首页, 发现了搜索框, 看到了默认搜索选项 All, 点击一看, 发现了 GitBooks 选项
        self.browser.get(self.server_url)
        search_button = self.browser.find_element_by_id("id_search")
        self.browser.find_element_by_id("id_current_search_choice").click()
        search_choices = self.browser.find_elements_by_id("id_search_choices")
        self.assertTrue(any(
            [pointed_choice in each_choice.text for each_choice in search_choices]
        ))

        # Y 点击 GitBooks 选项, 发现当前的搜索选项变成了 GitBooks
        for each_choice in search_choices:
            if pointed_choice == each_choice.text:
                selected_choice = each_choice
                selected_choice.click()
        current_search_choice = self.browser.find_element_by_id("id_current_search_choice")
        self.assertEqual(current_search_choice.text, pointed_choice)

        search_button.send_keys("{}\n".format(search_content))

    def do_gitbook_search(self, search_content):
        """
        从首页选择 GitBook 下拉菜单后, 进行 gitbook 搜索
        :param search_content: str(), 要搜索的关键字
        :return: None
        """
        self.do_choose_search("GitBooks", search_content)

    def do_articles_search(self, search_content):
        """
        从首页选择 Articles 下拉菜单后, 进行 Articles 搜索
        :param search_content: str(), 要搜索的关键字
        :return: None
        """
        self.do_choose_search("Articles", search_content)

    def do_journals_search(self, search_content):
        """
        从首页选择 Journals 下拉菜单后, 进行 Journals 搜索
        :param search_content: str(), 要搜索的关键字
        :return: None
        """
        self.do_choose_search("Journals", search_content)

    def do_code_search(self, search_content):
        """
        从首页选择 Code 下拉菜单后, 进行 Code 搜索
        :param search_content: str(), 要搜索的关键字
        :return: None
        """
        self.do_choose_search("Code", search_content)

    def do_all_search(self, search_content):
        """
        进行 ALL 搜索
        :param search_content: str(), 要搜索的关键字
        :return: None
        """
        # 默认是 ALL 搜索, 所以暂时不用 choose search 了
        # self.do_choose_search("All", search_content)

        # Y 打开首页, 看到了搜索按钮
        self.browser.get(self.server_url)
        search_button = self.browser.find_element_by_id("id_search")

        # Y 搜索对应内容
        search_button.send_keys("{}\n".format(search_content))

    @staticmethod
    def create_multiple_articles_with_or_without_code():
        has_code_content = """
```python
time.sleep
```
"""
        # 笔记库里存在两篇笔记, 都含有 time.sleep 关键词
        has_code = Article.objects.create(title="has_code", content=has_code_content)
        no_code = Article.objects.create(title="no_code", content="time.sleep")

        return has_code, no_code


class TestSearchSort(BasicSearch):
    """
    主要是测试搜索结果排序问题
    """

    def setUp(self):
        super().setUp()

        # 创建测试数据
        self.create_articles_test_db_data()
        self.create_work_journal_test_db_data()

    def test_search_result_sort(self):
        """
        测试搜索结果依赖于点击次数
        """
        # Y 打开首页, 发现了搜索按钮, 于是搜索 test
        self.do_all_search("test")

        # 搜索结果出来了, Y 发现笔记《xxx》排在第一位, 《yyy》排在第二位
        search_result = self.browser.find_elements_by_id("id_search_result_title")
        first_time_first_title = search_result[0].text
        first_time_second_title = search_result[1].text

        # 两份结果的标题不一样
        self.assertNotEqual(first_time_first_title, first_time_second_title)

        # Y 觉得第二个结果才是自己想要的, 于是点进去第二个结果进行查看
        search_result[1].click()  # 对应 Article

        # Y 想知道自己的点击次数会不会影响搜索结果排序, 于是狂点了 10 下
        for i in range(10):
            self.browser.back()
            search_result = self.browser.find_elements_by_id("id_search_result_title")
            search_result[1].click()

        # 点完之后, Y 回到首页, 再次搜索 test
        self.do_all_search("test")

        # 它发现果然排名变了, 刚才的第二个变成了现在的第一个, 刚才的第一个变成了第二个
        search_result = self.browser.find_elements_by_id("id_search_result_title")
        second_time_first_title = search_result[0].text
        second_time_second_title = search_result[1].text
        self.assertEqual(first_time_first_title, second_time_second_title)
        self.assertEqual(first_time_second_title, second_time_first_title)

    def test_search_result_sort_will_not_effect_by_url_visit(self):
        """
        测试搜索结果的排序不会因为 URL 的直接访问而改变
        """
        # Y 打开首页, 搜索关键词 test
        self.do_all_search("test")

        # 它发现结果出来了两篇文章, 第一篇是 《xxx》, 第二篇是 《yyy》
        search_result = self.browser.find_elements_by_id("id_search_result_title")
        first_time_first_title = search_result[0].text
        first_time_second_title = search_result[1].text

        # 它记下了第二篇的 URL, 想看看是不是能够通过刷 URL 访问量来提高第二篇的排名
        first_time_second_url = search_result[1].get_attribute("href")

        # Y 一口气访问了第二篇 10 次
        for i in range(10):
            self.browser.get(first_time_second_url)

        # Y 再次搜索关键词 test
        self.do_all_search("test")

        # 它发现结果居然还是一样, 第二篇的排名依旧是第二
        search_result = self.browser.find_elements_by_id("id_search_result_title")
        second_time_first_title = search_result[0].text
        second_time_second_title = search_result[1].text
        self.assertEqual(first_time_first_title, second_time_first_title)
        self.assertEqual(first_time_second_title, second_time_second_title)


class TestSearchDisplay(BasicSearch):
    """
    测试搜索结果界面的显示
    """

    def setUp(self):
        super().setUp()

        # 创建测试数据
        self.create_articles_test_db_data()
        self.test_gitbooks = list(self.create_gitbook_test_db_data())

    def test_search_result_display(self):
        """
        2017.02.18 左下角显示的不只是文章数, 还有日记数
        测试搜索的结果, 应该显示对应的文章及对应到的搜索内容
        """
        # Y 知道文章 <article_with_markdown> 有这么一个关键字 <markdown1>, 所在行内容为 <* test markdown1>
        # 于是 Y 搜索 markdown1, 看是否显示这篇文章及结果出来
        self.do_all_search("markdown1")

        # 搜索结果出来了, Y 看到了自己搜索的关键词
        search_keyword = self.browser.find_element_by_id("id_search").get_attribute("value")
        self.assertEqual(search_keyword, "markdown1")

        # Y 查看搜索结果, 发现其找到对应文章了
        search_result = self.browser.find_element_by_tag_name("body").text
        self.assertIn("article_with_markdown", search_result)

        # 显示对应搜索结果
        self.assertIn("test markdown1", search_result)

        # 左下角显示的标题是笔记总数
        sidebar = self.browser.find_element_by_id("id_sidebar").text
        self.assertIn("笔记总数", sidebar)

    def test_search_nothing_display(self):
        """
        测试搜索不到的时候显示的内容
        """
        # Y 随便打了个关键词, 看能搜索出什么
        self.do_all_search("随便打了什么肯定式不会搜索到的才对的啊")

        # Y 看见了提示信息, 提示什么都搜不到
        self.assertIn(const.EMPTY_ARTICLE_ERROR, self.browser.page_source)

        # 同时也确实找不到文章标题信息等
        with self.assertRaises(NoSuchElementException):
            self.browser.find_element_by_id("id_search_result_title")

    def test_search_result_can_show_line_number(self):
        # Y 搜索 test, 发现搜索结果里面每个对应结果的前面都有数字, Y 怀疑是不是行号?
        self.do_all_search("test")
        result_table = self.browser.find_element_by_class_name("search-result-box-table-td")
        self.assertTrue(str(result_table.text).isdigit())

        # Y 再次搜索 created, 它知道笔记 <super与init方法> 中 created 应该在第 12 行
        search_button = self.browser.find_element_by_id("id_search")
        search_button.clear()
        search_button.send_keys("{}\n".format("created"))
        result_table = self.browser.find_element_by_class_name("search-result-box-table-td")
        self.assertIn("12", result_table.text)

    def test_search_result_will_show_tag(self):
        """
        测试搜索结果会显示对应文章的标签信息
        """
        # Y 知道某篇内容含有 "same category" 的笔记包含有 tag, 于是 Y 搜索这篇笔记
        self.do_all_search("same category")

        # Y 知道这篇文章的 tag 名字是 Others 和 Others2, 所以界面中应该有这俩个单词, 并且这俩个单词使用了正确的样式
        tag_result = self.browser.find_elements_by_id("id_article_tag")

        self.assertTrue(any(
            ["Others" == x.text for x in tag_result]
        ))

        self.assertTrue(any(
            ["Others2" == x.text for x in tag_result]
        ))

    def test_gitbook_will_show_tag(self):
        """
        本案例测试的是搜索结果的显示中, GitBook 也会显示对应的 Tag 信息
        """
        # Y 知道某份 GitBook 是有关 test 的, 而且 Y 知道可以通过 xxx 搜索到这份 GitBook 笔记, 于是 Y 输入了 xxx 进行搜索
        self.do_gitbook_search("test")

        # 搜索结果出来了, Y 发现这份 GitBook 的笔记含有 Tag-test
        tag_results = self.browser.find_elements_by_id("id_article_tag")
        self.assertTrue(any(
            ["test" == x.text for x in tag_results]
        ))

    def test_search_result_tag_can_search(self):
        """
        测试搜索结果中显示出来的 tag 应该是可以进一步搜索的
        """
        # Y 想知道搜索页面中显示的 Tag 能不能继续搜索, 它知道有个 Others Tag, 想用这个 tag 来做测试
        test_tag_name = "Others"
        test_tag = Tag.objects.get(tag_name=test_tag_name)

        # Y 知道某篇笔记中含有 same category 这个内容, 且这篇笔记含有 Others 这个 tag, 于是 Y 想把这篇笔记搜索出来
        self.do_all_search("same category")
        search_result_url = self.browser.current_url

        # Y 知道搜索结果中肯定有一个 tag 是 Others, 于是在搜索结果中找它
        tags = self.browser.find_elements_by_id("id_article_tag")
        for each_tag in tags:
            if each_tag.text == "Others":
                each_tag.click()
                break

        # Y 发现 URL 变化了, 看上去像是对 Tag 进行了搜索的样子
        self.assertNotEqual(search_result_url, self.browser.current_url)

        # Y 知道笔记库中有 Others 这个 Tag 的笔记总共有 x 篇, 而且界面上刚好显示出来 x 篇笔记
        articles_has_test_tag = Article.objects.filter(tag=test_tag)
        articles_display = self.browser.find_elements_by_id("id_article_title")
        self.assertEqual(len(articles_has_test_tag), len(articles_display))


class TestSearchButton(BasicSearch):
    def setUp(self):
        super().setUp()

        # 创建测试数据
        self.create_articles_test_db_data()
        self.create_work_journal_test_db_data()
        self.test_gitbooks = list(self.create_gitbook_test_db_data())

    def test_can_search_title(self):
        """
        2016.10.04 测试能够搜索各个文章的标题即可
        :return:
        """
        # Y 打开首页, 看到了搜索按钮
        self.browser.get(self.server_url)
        search_button = self.browser.find_element_by_id("id_search")

        # Y 知道某篇已经存在的文章, 随便打了一个进去, 然后按下回车键
        newest_article = Article.objects.first()
        search_button.send_keys(newest_article.title + "\n")

        # 发现确实能够搜索出对应的文章出来
        self.assertIn(newest_article.title, self.browser.page_source)

        # Y 想试试如果搜索一篇不存在的文章会怎样, 就随便打了一串字符, 尝试进行搜索
        search_button = self.browser.find_element_by_id("id_search")
        search_button.send_keys("不应该有这篇文章的存在\n")

        # 发现搜索结果为: 没有相关文章题目
        self.assertIn(const.EMPTY_ARTICLE_ERROR, self.browser.page_source)

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
        articles_after_search = self.browser.find_element_by_id(const.ID_SEARCH_RESULT_TITLE)
        articles_after_search.click()
        self.assertIn("time.sleep", self.browser.find_element_by_tag_name('body').text)

        # Y 想知道这个搜索功能是否类似于 google 搜索, 即可以用空格来区分多个关键词然后进行搜索
        search_button = self.browser.find_element_by_id("id_search")

        # Y 搜索了这么一个关键词: and I, 发现确实搜出来结果了, 而且随便打开一片文章里面可以找到 and 和 I, 而且不是连在一起的
        search_button.send_keys("and I\n")
        articles_after_search = self.browser.find_element_by_id(const.ID_SEARCH_RESULT_TITLE)
        articles_after_search.click()
        body_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn("and", body_text)
        self.assertIn("I", body_text)
        self.assertNotIn("and I", body_text)

        # Y 尝试随便输入一些东西, 看是不是能搜出什么
        search_button = self.browser.find_element_by_id("id_search")
        search_button.send_keys("随便输入了一些什么啊肯定是搜索不到的\n")

        # 果然关键词打得太随意了, 啥都没有啊
        articles_after_search = self.browser.find_elements_by_id(const.ID_SEARCH_RESULT_TITLE)
        self.assertTrue(len(articles_after_search) == 0, "居然找到文章了?!")

    def test_can_search_among_article_journals_gitbooks(self):
        """
        测试主页的搜索既能搜索文章又能搜索日记还能搜索 gitbooks
        """
        # Y 打开首页, 看到了搜索按钮
        self.browser.get(self.server_url)
        search_button = self.browser.find_element_by_id("id_search")

        # Y 知道 test 这个关键词在文章和日记中都用到了, 于是搜索这个关键词
        search_button.send_keys("test\n")

        # Y 看见文章、日记、gitbook 都被搜索了出来
        self.assertIn("article_with_markdown", self.browser.page_source)
        self.assertIn("2017-02-08 任务情况总结", self.browser.page_source)
        self.assertTrue(any(
            [x.title in self.browser.page_source for x in self.test_gitbooks]
        ))

    def test_search_again(self):
        """
        发现第一次搜索的时候确实是链接到 all, 但是再次搜索的时候又变成 articles 了
        正确的情况应该两次都是 all 才对
        """
        # Y 打开首页, 看到了搜索按钮
        self.browser.get(self.server_url)
        search_button = self.browser.find_element_by_id("id_search")

        # Y 随便打了个关键词, 发现页面跳转了
        search_button.send_keys("随便打了什么肯定式不会搜索到的才对的啊\n")
        search_url = self.browser.current_url
        self.assertNotEqual(search_url, self.server_url)

        # Y 再次进行搜索, 这回输入了一个文章和日记里面都有的关键词
        search_button = self.browser.find_element_by_id("id_search")
        search_button.clear()
        search_button.send_keys("test\n")

        # 发现对应的日记和文章都被搜索出来了, 而且 url 保持不变
        self.assertEqual(search_url, self.browser.current_url)
        self.assertIn("article_with_markdown", self.browser.page_source)
        self.assertIn("2017-02-08 任务情况总结", self.browser.page_source)

    def test_search_choice_all(self):
        """
        测试搜索选项, 选择 All 的时候可以搜索包括 Articles、GitBooks、Journal 的内容
        """
        # Y 打开首页, 发现了搜索框的默认按钮, 是 All 选项
        self.browser.get(self.server_url)
        search_button = self.browser.find_element_by_id("id_search")
        search_choice = self.browser.find_element_by_id("id_current_search_choice")
        self.assertEqual(search_choice.text, "All")

        # Y 知道 Articles、GitBooks、Journals 中均有某篇笔记包含内容 <test>, 于是 Y 搜索 test
        search_button.send_keys("{}\n".format("test"))

        # 搜索结果出来了, 发现果然 Articles、GitBooks、Journals 中含有 test 的笔记都被搜索出来了
        search_results = self.browser.find_elements_by_class_name("search-result")
        self.assertTrue(any(
            ["article_with_markdown" in each_result.text for each_result in search_results])
        )
        self.assertTrue(any(
            ["2017-02-08 任务情况总结" in each_result.text for each_result in search_results])
        )
        self.assertTrue(any(
            ["test_book_name" in each_result.text for each_result in search_results])
        )

    def test_search_choice_articles(self):
        """
        测试搜索选项, 选择 Articles 的时候只能搜索包括 Articles 的内容
        """
        # Y 知道 Articles、GitBooks、Journals 中均有某篇笔记包含内容 <test>, 于是 Y 搜索 test
        # Y 希望搜索出来的结果不包含 GitBooks 和 Journals 的内容
        self.do_articles_search("test")

        # 搜索结果出来了, 果然只包含了 Articles 的内容
        search_results = self.browser.find_elements_by_class_name("search-result")
        self.assertTrue(any(
            ["article_with_markdown" in each_result.text for each_result in search_results])
        )
        self.assertFalse(any(
            ["2017-02-08 任务情况总结" in each_result.text for each_result in search_results])
        )
        self.assertFalse(any(
            ["test_book_name" in each_result.text for each_result in search_results])
        )

    def test_search_choice_gitbooks(self):
        """
        测试搜索选项, 选择 GitBooks 的时候只能搜索包括 GitBooks 的内容
        """
        # Y 知道 Articles、GitBooks、Journals 中均有某篇笔记包含内容 <test>, 于是 Y 搜索 test
        # Y 希望搜索出来的结果不包含 Articles 和 Journals 的内容
        self.do_gitbook_search("test")

        # 搜索结果出来了, 果然只包含了 GitBook 的内容
        search_results = self.browser.find_elements_by_class_name("search-result")
        self.assertFalse(any(
            ["article_with_markdown" in each_result.text for each_result in search_results])
        )
        self.assertFalse(any(
            ["2017-02-08 任务情况总结" in each_result.text for each_result in search_results])
        )
        self.assertTrue(any(
            ["test_book_name" in each_result.text for each_result in search_results])
        )

    def test_search_choice_journals(self):
        """
        测试搜索选项, 选择 Journals 的时候只能搜索包括 Journals 的内容
        """
        # Y 知道 Articles、GitBooks、Journals 中均有某篇笔记包含内容 <test>, 于是 Y 搜索 test
        # Y 希望搜索出来的结果不包含 GitBooks 和 Articles 的内容
        self.do_journals_search("test")

        # 搜索结果出来了, 果然只包含了 Journals 的内容
        search_results = self.browser.find_elements_by_class_name("search-result")
        self.assertFalse(any(
            ["article_with_markdown" in each_result.text for each_result in search_results])
        )
        self.assertTrue(any(
            ["2017-02-08 任务情况总结" in each_result.text for each_result in search_results])
        )
        self.assertFalse(any(
            ["test_book_name" in each_result.text for each_result in search_results])
        )

    def test_search_invalid_char(self):
        """
        测试搜索非法字符
        """
        # Y 打开首页, 看到了一个搜索框
        self.browser.get(self.server_url)
        home_url = self.browser.current_url
        search_button = self.browser.find_element_by_id("id_search")

        # 它想试试这个搜索框是不是有漏洞, 于是输入一个特殊字符
        search_button.send_keys("(\n")

        # Y 发现点击搜索之后, 又是回到了首页, 而且搜索框的内容被清空了
        search_button = self.browser.find_element_by_id("id_search")
        self.assertEqual(search_button.get_attribute("value"), "")
        self.assertEqual(self.browser.current_url, home_url)

        # Y 怀疑是不是不能输入单个字符, 于是输入多个, 发现结果一样
        search_button.send_keys("%^&*(\n")
        search_button = self.browser.find_element_by_id("id_search")
        self.assertEqual(search_button.get_attribute("value"), "")
        self.assertEqual(self.browser.current_url, home_url)

    def test_can_search_code(self):
        """
        测试能够搜索 code 代码
        """
        # 确保进行了代码更新
        code_collect()

        # 它选中了 Code, 打算对 Code 中的有关 time.sleep 进行搜索, 它知道某篇笔记肯定有关于这个的内容
        self.do_code_search("time.sleep")

        # 搜索 Code, 发现这篇笔记果然出现了
        search_results = self.browser.find_elements_by_class_name("search-result")
        self.assertTrue(any(
            ["article_with_markdown" in each_result.text for each_result in search_results])
        )

    def test_search_only_code_in_Article(self):
        """
        测试能够只搜索 code 代码, 测试 Article 内容
        """
        has_code, no_code = self.create_multiple_articles_with_or_without_code()

        # 确保进行了代码更新
        code_collect()

        # Y 搜索 "time.sleep", 发现只有 time.sleep 出现在 code 块的笔记被搜出来, 另外一份没有被搜出来
        self.do_code_search("time.sleep")

        search_results = self.browser.find_elements_by_id("id_search_result_title")
        self.assertTrue(any(
            [has_code.title == each_result.text for each_result in search_results])
        )

        self.assertFalse(any(
            [no_code.title == each_result.text for each_result in search_results])
        )

        current_url = self.browser.current_url
        # 点开文章, 发现页面跳转了, 笔记中确实有搜索的关键词
        for each_result in search_results:
            if has_code.title == each_result.text:
                each_result.click()
                break

        self.assertNotEqual(current_url, self.browser.current_url)
        self.assertEqual(has_code.title, self.browser.find_element_by_class_name("post-title").text)

    def test_search_only_code_in_Journal_can_link_correct(self):
        """
        测试 code 搜索 Journal 能够正确链接
        """
        journal_content = """
```python
print("Hello Journal")
```
"""

        today = datetime.datetime.today()
        journal, created = Journal.objects.get_or_create(
            title="{}-{}-{} 任务情况总结".format(today.year, today.month, today.day), date=today)
        journal.content = journal_content
        journal.save()

        # 确保 code 更新了
        code_collect()

        # Y 打开首页, 进行 code 搜索, 能够搜出这篇 journal
        self.do_code_search("print")

        # 能够看到搜索结果
        search_result = self.browser.find_elements_by_id("id_search_result_title")
        self.assertTrue(
            any(
                [journal.title == each_result.text for each_result in search_result]
            )
        )
        current_url = self.browser.current_url

        for each_result in search_result:
            if journal.title == each_result.text:
                each_result.click()
                break

        # Y 点击 journal 想看更详细的内容, 发现成功点开了
        self.assertNotEqual(current_url, self.browser.current_url)
        self.assertEqual(journal.title, self.browser.find_element_by_class_name("post-title").text)

    def test_search_gitbook_show_gitbook_name(self):
        """
        2017.04.30 之前的 GitBook title 很不规范, 现在要重新编写测试来规范化一下
        要求以如下格式显示: 《GitBook书名》-第几章第几节
        :return:
        """
        # 进行 gitbook 搜索
        self.do_gitbook_search("test")

        # 检查显示结果是否按照规范来显示
        search_results = self.browser.find_elements_by_class_name("search-result")
        for each_result in search_results:
            title = each_result.text.split("\n")[0]
            self.assertRegex(title, "《.+》-.+")


if __name__ == "__main__":
    pass
