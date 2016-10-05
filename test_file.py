#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" Description
"""
import locale
import sys
import os

__author__ = '__L1n__w@tch'

if __name__ == "__main__":
    with open(os.curdir + os.sep + "test.txt", "w") as f:
        print("test", file=f)
        print(locale.getlocale(), file=f)
        print(sys.getdefaultencoding(), file=f)
        print("啊啊啊", file=f)
