#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.05.21 添加字段 click_times, 用来表示访问次数的
2017.03.15 要提供搜索选项的功能, 需要重构一下搜索的 Form, 甚至连对应的 Model 都要修改
"""

# 标准库
from django.db import models
from django.urls import reverse

# 自己的模块
import my_constant as const


class SearchModel(models.Model):
    search_content = models.CharField(max_length=100, blank=False, help_text=const.SEARCH_CONTENT_HELP_TEXT)
    SEARCH_CHOICES = (
        ("all", "All"),
        ("gitbooks", "Gitbooks"),
        ("articles", "Articles"),
        ("journals", "Journals"),
        ("code", "Code"),
    )
    search_choice = models.CharField(max_length=10, choices=SEARCH_CHOICES,
                                     blank=False, help_text=const.SEARCH_CHOICE_HELP_TEXT)

    def save(self, *args, **kwargs):
        self.search_content = self.search_content.lower()
        if not any([each_choice[0] == self.search_choice.lower() for each_choice in self.SEARCH_CHOICES]):
            raise RuntimeError
        else:
            self.search_choice = self.search_choice.lower()
        self.title = self.search_content
        super().save(*args, **kwargs)


class BaseModel(models.Model):
    title = models.CharField(max_length=100, blank=False, unique=True)  # 文章或日记的题目
    category = models.CharField(max_length=50)  # 博客分类
    content = models.TextField(null=True, default=str())  # 博客文章正文
    click_times = models.IntegerField(default=0)  # 被访问次数

    # python3使用__str__
    def __str__(self):
        return self.title


class Tag(models.Model):
    tag_name = models.CharField(max_length=64)

    def __str__(self):
        return self.tag_name


class Article(BaseModel):
    tag = models.ManyToManyField(Tag, blank=True)  # 博客标签, 可为空
    create_time = models.DateTimeField(auto_now_add=True)  # 文章创建日期
    update_time = models.DateTimeField(auto_now_add=True)  # 文章更新日期

    def __init__(self, *args, **kwargs):
        super(Article, self).__init__(*args, **kwargs)

        # 博客分类, 默认值为 Others
        Article._meta.get_field('category').default = "Others"

    def get_absolute_url(self):
        path = reverse('detail', kwargs={'article_id': self.id})
        return "http://127.0.0.1:8000{}".format(path)

    class Meta:
        ordering = ['-update_time']
