#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 测试凯撒密码的加解密

2017.10.14 补充凯撒加密的例子
"""
from django.test import TestCase

from toolhub.cryptography.caesar_cipher import Caesar

__author__ = '__L1n__w@tch'


class TestCaesar(TestCase):
    def setUp(self):
        self.test_string = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        self.shift = 28
        self.answer_string = "cdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZab"

    def test_caesar(self):
        caesar = Caesar(self.test_string)
        cipher_text = caesar.encrypt(self.test_string, self.shift)
        self.assertTrue(cipher_text == self.answer_string)
        plaintext = caesar.decrypt(self.answer_string, self.shift)
        self.assertTrue(plaintext == self.test_string)

    def test_dictionary(self):
        """
        测试使用默认字典的情况
        :return:
        """
        caesar = Caesar()
        cipher_text = caesar.encrypt(self.test_string, self.shift)
        self.assertTrue(cipher_text == self.answer_string)
        plaintext = caesar.decrypt(self.answer_string, self.shift)
        self.assertTrue(plaintext == self.test_string)

    def test_demo(self):
        """
        测试使用默认字典的几个例子
        :return:
        """
        caesar = Caesar()
        test_data = "zobD*ooC", 5
        right_answer = "ujW8*jj7"
        my_answer = caesar.decrypt(*test_data)
        self.assertEqual(right_answer, my_answer)

        test_data = "zobD*ooC", 7
        right_answer = "shU6*hh5"
        my_answer = caesar.decrypt(*test_data)
        self.assertEqual(right_answer, my_answer)

        test_data = "zobD*ooC", 31
        right_answer = "UJ6i*JJh"
        my_answer = caesar.decrypt(*test_data)
        self.assertEqual(right_answer, my_answer)

        test_data = "UJ6i*JJh", 31
        right_answer = "zobD*ooC"
        my_answer = caesar.decrypt(*test_data)
        self.assertEqual(right_answer, my_answer)
