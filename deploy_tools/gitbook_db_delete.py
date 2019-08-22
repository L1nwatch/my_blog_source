#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 清空 gitbook 表里所有数据
"""
import peewee
import urllib.parse
import pypinyin
import string

__author__ = '__L1n__w@tch'


class Articles_BaseModel(peewee.Model):
    class Meta:
        database = peewee.SqliteDatabase("/home/watch/sites/watch0.top/source/my_blog/db.sqlite3")


class Gitbook_Notes_Gitbook(Articles_BaseModel):
    basemodel_ptr_id = peewee.PrimaryKeyField()
    href = peewee.CharField()
    book_name = peewee.CharField()


def change_url(raw_url, book_name):
    """

    :param raw_url:
    :param book_name:
    :return:
    """
    book_name = book_name.lower()
    raw_url = raw_url[len("https://l1nwatch.gitbooks.io/{}/content/".format(book_name)):]
    if raw_url.endswith("/readme.html"):
        raw_url = raw_url[:-len("/readme.html")]
    if raw_url.endswith("index.html"):
        raw_url = raw_url[:-len("index.html")]
    if raw_url.endswith(".html"):
        raw_url = raw_url[:-len(".html")]

    result_url = list()
    for each_split in raw_url.split("/"):
        temp_split = urllib.parse.unquote(each_split)
        string_set = (set(string.punctuation) - set("-")).union(set(string.whitespace))
        for each_sp_char in string_set:
            temp_split = temp_split.replace(each_sp_char, "")
        temp_split = "-".join(pypinyin.lazy_pinyin(temp_split)).lower()
        result_url.append(temp_split)
    result_url = "/".join(result_url)

    right_url = "https://l1nwatch.gitbook.io/{}/{}"
    return right_url.format(book_name, result_url)


if __name__ == "__main__":
    for each in Gitbook_Notes_Gitbook.select():
        # print(each.href)
        # print(each.book_name)
        new_url = change_url(each.href, each.book_name)
        each.href = new_url
        each.save()
