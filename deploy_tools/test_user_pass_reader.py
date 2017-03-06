#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.03.05 新增了一个 fab 配置 gitbooks 的操作, 但还是懒得写测试, 于是依旧手调
2017.02.10 写测试好懒, 还是手调吧
2017.02.03 由于自己的 git 为私有 git, 需要通过配置文件读取 git 账号密码, 所以需要编写函数进行测试
"""
from fabfile import _user_pass_file_config, _gitbooks_config

__author__ = '__L1n__w@tch'

if __name__ == "__main__":
    # _user_pass_file_config()
    _gitbooks_config("/Users/L1n/Desktop/Code/Python/my_blog_source", site_name="my_blog")
