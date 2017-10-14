#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 凯撒密码的代码实现

2017.10.14 将之前写的凯撒加密迁移进来
"""
import string

__author__ = '__L1n__w@tch'

DEFAULT_DICTIONARY = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"


class Caesar:
    def __init__(self, dictionary=DEFAULT_DICTIONARY):
        self.dictionary = dictionary  # 加解密所用的字典

    def encrypt(self, text, shift):
        """
        凯撒密码的加密操作
        :param text: "Valar Morghulis"
        :param shift: 偏移量, 比如 13
        :return: "inynE ZBEtuHyvF"
        """
        result = str()
        for char in text:
            if char in self.dictionary:
                result += self.dictionary[(self.dictionary.index(char) + shift) % len(self.dictionary)]
            else:
                result += char

        return result

    def decrypt(self, text, shift):
        """
        凯撒密码的解密操作
        :param text: "inynE ZBEtuHyvF"
        :param shift: 偏移量, 比如 13
        :return: "Valar Morghulis"
        """
        return self.encrypt(text, -shift)


if __name__ == "__main__":
    caesar = Caesar(string.ascii_letters)
    cipher_text = caesar.encrypt("Valar Morghulis", 13)
    plaintext = caesar.decrypt(cipher_text, 13)
    print("明文: {}, 密文: {}, 偏移量为: {}".format(plaintext, cipher_text, 13))
