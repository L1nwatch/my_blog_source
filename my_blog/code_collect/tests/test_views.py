#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 为视图编写相关测试代码

2017.04.04 重构一下创建测试数据的代码
2017.03.31 修正一下 code 搜索出来的链接不正确的问题, 完善对应测试
2017.03.30 编写有关搜索部分的相关测试
2017.03.29 编写有关更新代码块数据库的相关测试
"""
from articles.models import Article
from articles.tests.basic_test import BasicTest
from code_collect.models import CodeCollect
from my_constant import const

from code_collect.views import (code_collect, get_all_code_type_in_note, parse_query,
                                get_note_type, get_all_code_area, search_code_keyword_in_note)

__author__ = '__L1n__w@tch'


class BasicFunction(BasicTest):
    def create_article_with_code(self):
        """
        创建含有 code 的 article
        :return: article 实例
        """
        code_content = """
```python
print("Hello CodeCollect! I am Article")
```
"""
        return self.create_article(content=code_content)

    def create_journal_with_code(self):
        """
        创建含有 code 的 journal
        :return: journal 实例
        """
        content = """
```python
print("Hello CodeCollect! I am Journal")
```
"""
        return self.create_journal(content=content)

    def create_gitbook_with_code(self):
        """
        创建含有 code 的 GitBook
        :return: gitbook 实例
        """
        content = """
```python
print("Hello CodeCollect! I am GitBook")
```
"""

        return self.create_gitbook(content=content)

    def create_article_with_multiple_code(self):
        """
        创建含有多个 code 块的 article
                :return: article 实例
        """
        content = """
```python
print("Hello CodeCollect! I am Article")
```

```shell
echo "Hello CodeCollect! I am Article with shell output"
```
"""
        return self.create_article(content=content)

    def create_code_associate_with_article(self, article=None):
        """
        创建与 article 相关的 code 数据
        """
        if not article:
            article = self.create_article_with_code()
        return self.create_code(code_type="python", note=article)

    def create_article_without_code(self):
        """
        创建不包含代码块的 article
        :return: article 实例
        """
        content = "print('Hello!')"
        return self.create_article(content=content)


class CodeUpdateTest(BasicFunction):
    def test_can_update_article_code(self):
        """
        测试可以更新 Article 笔记库中的相关信息
        """
        # 笔记库中存在某篇 Article 符合收集条件
        article = self.create_article_with_code()

        # 调用 code_collect 函数
        code_collect()

        # 发现成功收录了进来
        CodeCollect.objects.get(note=article)

    def test_can_update_gitbook_code(self):
        """
        测试可以更新 GitBook 笔记库中的相关信息
        """
        # 笔记库中存在某篇 GitBook 符合收集条件
        gitbook = self.create_gitbook_with_code()

        # 调用 code_collect 函数
        code_collect()

        # 发现成功收录了进来
        CodeCollect.objects.get(note=gitbook)

    def test_can_update_journal_code(self):
        """
        测试可以更新 Journal 笔记库中的相关信息
        :return:
        """
        # 笔记库中存在某篇 GitBook 符合收集条件
        journal = self.create_journal_with_code()

        # 调用 code_collect 函数
        code_collect()

        # 发现成功收录了进来
        CodeCollect.objects.get(note=journal)

    def test_will_delete_with_article(self):
        """
        测试当 article 被删除时, 对应的 Code 信息也删除了
        :return:
        """
        article = self.create_article_with_code()
        code_collect()

        # 确保已经有 article
        CodeCollect.objects.get(note=article)

        # 删除 Article
        article.delete()

        # 再次查找, 已经找不到了
        with self.assertRaises(CodeCollect.DoesNotExist):
            CodeCollect.objects.get(note=article)

    def test_will_delete_with_gitbooks(self):
        """
        测试当 gitbook 被删除时, 对应的 Code 信息也删除了
        :return:
        """
        gitbook = self.create_gitbook_with_code()
        code_collect()

        # 确保已经有 gitbook
        CodeCollect.objects.get(note=gitbook)

        # 删除 Article
        gitbook.delete()

        # 再次查找, 已经找不到了
        with self.assertRaises(CodeCollect.DoesNotExist):
            CodeCollect.objects.get(note=gitbook)

    def test_will_delete_with_journal(self):
        """
        测试当 journal 被删除时, 对应的 Code 信息也删除了
        :return:
        """
        journal = self.create_journal_with_code()
        code_collect()

        # 确保已经有 journal
        CodeCollect.objects.get(note=journal)

        # 删除 Article
        journal.delete()

        # 再次查找, 已经找不到了
        with self.assertRaises(CodeCollect.DoesNotExist):
            CodeCollect.objects.get(note=journal)

    def test_will_sync_with_article(self):
        """
        测试当 article 更新的时候, 对应的 Code 信息也会进行更新
        :return:
        """
        article = self.create_article_with_code()
        code_collect()

        # 确保已经有 article
        code = CodeCollect.objects.get(note=article)
        self.assertEqual(code.code_type, "python")

        # article 内容被更新
        article.content = """
```c++
cout << "Hello CodeCollect! I am Article!"
```
"""
        article.save()

        # 再次调用
        code_collect()

        # 发现确实更新了
        self.assertTrue(
            any(
                [each_code.code_type == "c++" for each_code in CodeCollect.objects.filter(note=article)]
            )
        )

        # article 现在没有代码块了
        article.content = "Hello CodeCollect! I am Article!"
        article.save()
        code_collect()

        # code 也找不到了
        with self.assertRaises(CodeCollect.DoesNotExist):
            CodeCollect.objects.get(note=article)

    def test_will_sync_with_gitbook(self):
        """
        测试当 gitbook 更新的时候, 对应的 Code 信息也会进行更新
        :return:
        """
        gitbook = self.create_gitbook_with_code()
        code_collect()

        # 确保已经有 gitbook
        code = CodeCollect.objects.get(note=gitbook)
        self.assertEqual(code.code_type, "python")

        # gitbook 内容被更新
        gitbook.content = """
```c++
cout << "Hello CodeCollect! I am Article!"
```
        """
        gitbook.save()

        # 再次调用
        code_collect()

        # 发现确实更新了
        code = CodeCollect.objects.get(note=gitbook)
        self.assertEqual(code.code_type, "c++")

        # gitbook 现在没有代码块了
        gitbook.content = "Hello CodeCollect! I am Gitbook!"
        gitbook.save()
        code_collect()

        # code 也找不到了
        with self.assertRaises(CodeCollect.DoesNotExist):
            CodeCollect.objects.get(note=gitbook)

    def test_will_sync_with_journal(self):
        """
        测试当 journal 更新的时候, 对应的 Code 信息也会进行更新
        """
        journal = self.create_journal_with_code()
        code_collect()

        # 确保已经有 journal
        code = CodeCollect.objects.get(note=journal)
        self.assertEqual(code.code_type, "python")

        # journal 内容被更新
        journal.content = """
```c++
cout << "Hello CodeCollect! I am Journal!"
```
        """
        journal.save()

        # 再次调用
        code_collect()

        # 发现确实更新了
        code = CodeCollect.objects.get(note=journal)
        self.assertEqual(code.code_type, "c++")

        # journal 现在没有代码块了
        journal.content = "Hello CodeCollect! I am Journal!"
        journal.save()
        code_collect()

        # code 也找不到了
        with self.assertRaises(CodeCollect.DoesNotExist):
            CodeCollect.objects.get(note=journal)

    def test_can_collect_multiple_code_type(self):
        """
        测试能够搜集一份笔记里面的多份 code_type
        """
        article = self.create_article_with_multiple_code()

        # 更新 code 库, 应该有两条记录
        code_collect()

        # 两条都能获取到
        CodeCollect.objects.get(note=article, code_type="shell")
        CodeCollect.objects.get(note=article, code_type="python")

    def test_get_all_code_type_in_note(self):
        test_note = Article.objects.create(title="test", content="""
```python
print("Hello")
# ```
```

```c++
print("No Hello")
```
""")
        right_answer = ["python", "c++"]
        my_answer = get_all_code_type_in_note(test_note)
        self.assertEqual(right_answer, my_answer)


class CodeSearchTest(BasicFunction):
    unique_url = "/search/"

    def test_can_search_code(self):
        """
        测试搜索功能, 能够正常进行 code 的搜索
        """
        code = self.create_code_associate_with_article()

        response = self.client.post(self.unique_url, data={"search_content": "print",
                                                           "search_choice": "code"})

        self.assertContains(response, code.note.title)

    def test_only_search_code(self):
        """
        测试搜索功能, 只对笔记中的 code 部分进行搜索
        """
        code = self.create_code_associate_with_article()
        article = self.create_article_without_code()

        response = self.client.post(self.unique_url, data={"search_content": "print",
                                                           "search_choice": "code"})
        self.assertContains(response, code.note.title)
        self.assertNotContains(response, article.title)

    def test_search_without_case(self):
        """
        测试搜索时无视大小写
        """
        code = self.create_code_associate_with_article()

        response = self.client.post(self.unique_url, data={"search_content": "prInT",
                                                           "search_choice": "code"})
        self.assertContains(response, code.note.title)

    def test_search_in_pointed_code_type(self):
        """
        测试搜索时仅从指定类型的代码中进行搜索
        """
        code = self.create_code_associate_with_article()

        response = self.client.post(self.unique_url, data={"search_content": "python print",
                                                           "search_choice": "code"})
        self.assertContains(response, code.note.title)

        response = self.client.post(self.unique_url, data={"search_content": "c++ print",
                                                           "search_choice": "code"})
        self.assertNotContains(response, code.note.title)

    def test_parse_query(self):
        test_data = "python print"
        right_answer = {"print"}, "python"
        my_answer = parse_query(test_data)
        self.assertEqual(right_answer, my_answer)

        test_data = "python"
        right_answer = {"python"}, ""
        my_answer = parse_query(test_data)
        self.assertEqual(right_answer, my_answer)

        test_data = "c++ python print"
        right_answer = {"python", "print"}, "c++"
        my_answer = parse_query(test_data)
        self.assertEqual(right_answer, my_answer)

    def test_get_note_type(self):
        """
        测试获取 note 类型是否正确
        """
        article = self.create_article_with_code()
        self.assertEqual(get_note_type(article), "articles")

        gitbook = self.create_gitbook_with_code()
        self.assertEqual(get_note_type(gitbook), "gitbook_notes")

        journal = self.create_journal_with_code()
        self.assertEqual(get_note_type(journal), "work_journal")

        code = self.create_code_associate_with_article(article)
        self.assertEqual(get_note_type(code), "code")

        self.assertEqual(get_note_type(code.note), "articles")

    def test_get_all_code_area(self):
        """
        测试获取笔记的代码块
        """
        article = self.create_article_with_code()
        right_answer = ['print("Hello CodeCollect! I am Article")']
        my_answer = get_all_code_area(article, "python")
        self.assertEqual(right_answer, my_answer)

        article = self.create_article_without_code()
        right_answer = []
        my_answer = get_all_code_area(article, "python")
        self.assertEqual(right_answer, my_answer)

        # 测试获取所有语言
        article = self.create_article_with_multiple_code()
        right_answer = ['print("Hello CodeCollect! I am Article")',
                        'echo "Hello CodeCollect! I am Article with shell output"']
        my_answer = get_all_code_area(article, "")
        self.assertEqual(right_answer, my_answer)

        # 测试只获取 Python 语言
        right_answer = ['print("Hello CodeCollect! I am Article")']
        my_answer = get_all_code_area(article, "python")
        self.assertEqual(right_answer, my_answer)

        # 测试只获取 Shell 语言
        right_answer = ['echo "Hello CodeCollect! I am Article with shell output"']
        my_answer = get_all_code_area(article, "shell")
        self.assertEqual(right_answer, my_answer)

    def test_search_code_keyword_in_note(self):
        """
        测试在某篇笔记中搜索对应的关键词
        """
        article = self.create_article_with_code()
        keyword_set = {"print"}
        all_code_area = ['print("Hello CodeCollect! I am Article")']
        # 注意这里的代码行号表示在代码块里的行号, 而不是整篇文章里的
        right_answer = [const.SEARCH_RESULT_INFO("print", all_code_area[0], 1)]
        my_answer = search_code_keyword_in_note(article, keyword_set, all_code_area)
        self.assertEqual(right_answer, my_answer)

        keyword_set = {"AbCdEfg"}
        all_code_area = ['print("Hello CodeCollect! I am Article")']
        # 注意这里的代码行号表示在代码块里的行号, 而不是整篇文章里的
        right_answer = list()
        my_answer = search_code_keyword_in_note(article, keyword_set, all_code_area)
        self.assertEqual(right_answer, my_answer)

        article = self.create_article_with_multiple_code()
        keyword_set = {"shell"}
        all_code_area = ['print("Hello CodeCollect! I am Article")',
                         'echo "Hello CodeCollect! I am Article with shell output"']
        # 注意这里的代码行号表示在代码块里的行号, 而不是整篇文章里的
        right_answer = [const.SEARCH_RESULT_INFO("shell", all_code_area[1], 1)]
        my_answer = search_code_keyword_in_note(article, keyword_set, all_code_area)
        self.assertEqual(right_answer, my_answer)


if __name__ == "__main__":
    pass
