#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 各个功能测试的基类
"""
import sys
import os
import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from articles.models import Article, Tag
from work_journal.models import Journal

from datetime import datetime

DEFAULT_WAIT = 5
SCREEN_DUMP_LOCATION = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "screendumps")
)

__author__ = '__L1n__w@tch'


class FunctionalTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        """
        setUpClass 方法和 setUp 类似，也由 unittest 提供，但是它用于设定整个类的测试背景。
        也就是说，setUpClass 方法只会执行一次，而不会在每个测试方法运行前都执行。
        LiveServerTestCase 和 StaticLiveServerCase 一般都在这个方法中启动测试服务器。
        :return:
        """
        for arg in sys.argv:  # 在命令行中查找参数 liveserver(从 sys.argv 中获取)
            if "liveserver" in arg:
                # 如果找到了，就让测试类跳过常规的 setUpClass 方法，把过渡服务器的 URL 赋值给 server_url 变量
                cls.server_host = arg.split("=")[1]
                # 如果检测到命令行参数中有 liveserver, 就不仅存储 cls.server_url 属性，还存储 server_host 和 against_staging 属性
                cls.server_url = "http://" + cls.server_host
                cls.against_staging = True
                return
        super().setUpClass()
        cls.against_staging = False
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if not cls.against_staging:
            super().tearDownClass()

    def setUp(self):
        """
        setUp 是特殊的方法, 在各个测试方法之前运行。
        使用这个方法打开浏览器。
        :return:
        """
        # 在两次测试之间还原服务器中数据库的方法
        # if self.against_staging:
        #     reset_database(self.server_host)
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(DEFAULT_WAIT)  # 等待 DEFAULT_WAIT 秒钟

    def tearDown(self):
        """
        tearDown 是特殊的方法, 在各个测试方法之后运行。使用这个方法关闭浏览器.
        注意, 这个方法有点类似 try/except 语句, 就算测试中出错了, 也会运行 tearDown 方法(如果 setUp 出错了就不会执行这个方法).
        所以测试结束后, Firefox 窗口不会一直停留在桌面上了.
        :return:
        """
        # 截图功能
        if self._test_has_failed():
            if not os.path.exists(SCREEN_DUMP_LOCATION):
                os.makedirs(SCREEN_DUMP_LOCATION)
            for ix, handle in enumerate(self.browser.window_handles):
                self._windowid = ix
                self.browser.switch_to.window(handle)
                self.take_screenshot()
                self.dump_html()
        self.browser.quit()
        super().tearDown()

    def _test_has_failed(self):
        # 针对 3.4。在 3.3 中可以直接使用 self._outcomeForDoCleanups.success:
        for method, error in self._outcome.errors:
            if error:
                return True
        return False

    def take_screenshot(self):
        filename = self._get_filename() + ".png"
        print("screenshotting to", filename)
        self.browser.get_screenshot_as_file(filename)

    def dump_html(self):
        filename = self._get_filename() + ".html"
        print("dumping page HTML to", filename)
        with open(filename, "w") as f:
            f.write(self.browser.page_source)

    def _get_filename(self):
        timestamp = datetime.now().isoformat().replace(":", ".")[:19]
        return "{folder}/{classname}.{method}-window{windowid}-{timestamp}".format(folder=SCREEN_DUMP_LOCATION,
                                                                                   classname=self.__class__.__name__,
                                                                                   method=self._testMethodName,
                                                                                   windowid=self._windowid,
                                                                                   timestamp=timestamp)

    def wait_for_element_with_id(self, element_id):
        WebDriverWait(self.browser, timeout=50).until(
            lambda b: b.find_element_by_id(element_id), "Could not find element with id {}. Page text was {}"
                .format(element_id, self.browser.find_element_by_tag_name("body").text))

    @staticmethod
    def wait_for(function_with_assertion, timeout=DEFAULT_WAIT):
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                return function_with_assertion()
            except (AssertionError, WebDriverException):
                time.sleep(0.1)
        # 再试一次，如果还不行就抛出所有异常
        return function_with_assertion()

    @staticmethod
    def _create_articles_test_db_data():
        """
        创建测试用的相关数据
        :return:
        """
        # 创建三个标签, Python, Markdown, Others
        tag_python = Tag.objects.create(tag_name="Python")
        tag_markdown = Tag.objects.create(tag_name="Markdown")
        tag_others = Tag.objects.create(tag_name="Others")

        # 创建一篇文章, 分类为默认值 Others, 无标签, 内容为默认值空
        Article.objects.create(title="article_with_nothing")

        # 创建一篇文章, 分类为默认值 Others, 无标签, 有内容
        Article.objects.create(title="article_with_no_tag_category", content="I only have content and title")

        # 创建一篇文章, 有分类, 无标签, 有内容
        Article.objects.create(title="article_with_markdown", category="Markdown", content="""
## I am 2nd title
* test markdown1
* test markdown2
* test markdown3 and `inline code`

```python
import time

while True:
    time.sleep(50)
    print "hello world!"
```""")

        # 创建文章二, 有分类, 有标签, 有内容
        new_article = Article.objects.create(title="article_with_python", category="Python",
                                             content="I am `Python`")
        new_article.tag = (tag_python,)

        # 创建三篇文章, 带标签 Others 以及分类 Test_Category
        for i in range(3):
            new_article = Article.objects.create(title="article_with_same_category{}".format(i + 1),
                                                 category="Test_Category", content="Same category {}".format(i + 1))
            new_article.tag = (tag_others,)

        pass

    @staticmethod
    def _create_work_journal_test_db_data():
        Journal.objects.create(title="2017-02-03 任务情况总结"
                               , content="测试笔记, 应该记录 2017/02/03 的工作内容", date=datetime.today())


if __name__ == "__main__":
    pass
