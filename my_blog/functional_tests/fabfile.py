#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 为了实现远程调试执行管理命令
"""
from fabric.api import env, run

__author__ = '__L1n__w@tch'

# def _get_base_folder(host):
#     return "~/sites/" + host


# def _get_manage_dot_py(host):
#     raise RuntimeError("存在尚未修改的地方")  # TODO: 这里只是复制原来的代码, 需要改动
#     return "{path}/virtualenv/bin/python {path}/source/todo_app/manage.py".format(path=_get_base_folder(host))


# def reset_database():
#     run("{manage_py} flush --noinput".format(manage_py=_get_manage_dot_py(env.host)))


# def create_session_on_server(email):
#     session_key = run(
#         "{manage_py} create_session {email}".format(manage_py=_get_manage_dot_py(env.host), email=email))
#     print(session_key)


if __name__ == "__main__":
    pass
