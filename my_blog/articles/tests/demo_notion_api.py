#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2023.03.12 try notion api for searching notes
"""
import requests, json

__author__ = '__L1n__w@tch'


def search_by_title(search_content, headers):
    url = "https://api.notion.com/v1/search"
    post_data = {"query": "notion", "page_size": 100}
    post_data = json.dumps(post_data)
    response = requests.post(url, data=post_data, headers=headers)
    print(response.text)

    with open("demo.json", encoding="utf8", mode="w") as f:
        f.write(response.text)


def demo():
    token = 'None'

    headers = {
        "Authorization": f'Bearer {token}',
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    search_content = "aaa"
    search_by_title(search_content, headers)


if __name__ == "__main__":
    demo()
