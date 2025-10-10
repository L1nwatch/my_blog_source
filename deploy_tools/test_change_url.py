#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" Description
"""
from unittest import TestCase
from .gitbook_db_delete import change_url

__author__ = '__L1n__w@tch'

if __name__ == "__main__":
    pass


class TestChange_url(TestCase):
    def test_change_url(self):
        test_data = (
            "https://l1nwatch.gitbooks.io/pythonweb/content/PythonWeb%E5%BC%80%E5%8F%91%3A%20%E6%B5%8B%E8%AF%95%E9%A9%B1%E5%8A%A8%E6%96%B9%E6%B3%95/readme.html",
            "PythonWeb")
        right_answer = "https://l1nwatch.gitbook.io/pythonweb/pythonweb-kai-fa-ce-shi-qu-dong-fang-fa"
        my_answer = change_url(*test_data)
        self.assertEqual(right_answer, my_answer)

    def test_change_url2(self):
        test_data = (
            "https://l1nwatch.gitbooks.io/pythonweb/content/PythonWeb%E5%BC%80%E5%8F%91%3A%20%E6%B5%8B%E8%AF%95%E9%A9%B1%E5%8A%A8%E6%96%B9%E6%B3%95/%E5%87%86%E5%A4%87%E5%B7%A5%E4%BD%9C%E5%92%8C%E5%BA%94%E5%85%B7%E5%A4%87%E7%9A%84%E7%9F%A5%E8%AF%86/readme.html",
            "PythonWeb")
        right_answer = "https://l1nwatch.gitbook.io/pythonweb/pythonweb-kai-fa-ce-shi-qu-dong-fang-fa/zhun-bei-gong-zuo-he-ying-ju-bei-de-zhi-shi"
        my_answer = change_url(*test_data)
        self.assertEqual(right_answer, my_answer)

    def test_change_url3(self):
        test_data = (
            "https://l1nwatch.gitbooks.io/interview_exercise/content/stackoverflow-about-Python/%E5%8D%95%E4%B8%8B%E5%88%92%E7%BA%BF%E5%92%8C%E5%8F%8C%E4%B8%8B%E5%88%92%E7%BA%BF%E7%9A%84%E5%90%AB%E4%B9%89.html",
            "interview_exercise")
        right_href = "https://l1nwatch.gitbook.io/interview_exercise/stackoverflow-about-python/dan-xia-hua-xian-he-shuang-xia-hua-xian-de-han-yi"
        my_answer = change_url(*test_data)
        self.assertEqual(right_href, my_answer)

    def test_change_url4(self):
        test_data = ("https://l1nwatch.gitbooks.io/interview_exercise/content/index.html", "interview_exercise")
        right_href = "https://l1nwatch.gitbook.io/interview_exercise/"
        my_answer = change_url(*test_data)
        self.assertEqual(right_href, my_answer)

    def test_change_url5(self):
        test_data = ("https://l1nwatch.gitbooks.io/interview_exercise/content/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%9F%A5%E8%AF%86/readme2.html", "interview_exercise")
        right_href = "https://l1nwatch.gitbook.io/interview_exercise/ji-suan-ji-zhi-shi/readme2"
        my_answer = change_url(*test_data)
        self.assertEqual(right_href, my_answer)
