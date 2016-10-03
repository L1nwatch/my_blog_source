#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 书中没有提到,自己写了这个
"""
from os import path
import subprocess

__author__ = '__L1n__w@tch'

THIS_FOLDER = path.abspath(path.dirname(__file__))
SSH_PORT = 26832


def create_session_on_server(host, email):
    result = subprocess.check_output(
        [
            "fab",
            # 可以看出，在命令行中指定 fab 函数的参数使用的句法很简单，冒号后跟着 "变量=参数" 形式的写法
            "create_session_on_server:email={}".format(email),
            "--host={}:{}".format(host, SSH_PORT),  # 自己的服务器使用 SSH_PORT 端口号
            # 因为这些工作通过 Fabric 和子进程完成，而且在服务器中运行，所以从命令行的输出中提取字符串形式的会话键时一定要格外小心
            # "--hide=everything,status",
            "--hide=everything"
        ],
        cwd=THIS_FOLDER
    ).splitlines()[0].decode().strip()
    return result


def reset_database(host):
    subprocess.check_call(
        ["fab", "reset_database", "--host={}:{}".format(host, SSH_PORT)],
        cwd=THIS_FOLDER
    )


if __name__ == "__main__":
    pass
