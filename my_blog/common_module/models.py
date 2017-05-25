#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 通用模块的 model

2017.05.25 为 IP 表创建 model
"""
from django.db import models

__author__ = '__L1n__w@tch'


class VisitedIP(models.Model):
    ip_address = models.CharField(max_length=100, blank=False, unique=True)
    times = models.IntegerField(default=0)

    def __str__(self):
        return self.ip_address


if __name__ == "__main__":
    pass
