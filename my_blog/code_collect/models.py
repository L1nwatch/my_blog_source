#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" code_collect 相关 model

2017.03.28 新增相关 model, 用于保存代码块信息
"""
from articles.models import BaseModel
from django.db import models


class CodeCollect(models.Model):
    code_type = models.CharField(max_length=20, blank=False, null=False)
    note = models.ForeignKey(BaseModel, on_delete=models.CASCADE, null=False, blank=False)

    def save(self, *args, **kwargs):
        self.code_type = self.code_type.lower()
        super().save(*args, **kwargs)
