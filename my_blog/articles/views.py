#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X

from django.shortcuts import render, redirect
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

from .models import Article
from .forms import ArticleForm, EMPTY_ARTICLE_ERROR

import os
import chardet

HOME_PAGE_ARTICLES_NUMBERS = 2
TEST_GIT_REPOSITORY = settings.TEST_GIT_REPOSITORY
NOTES_PATH_NAME = "notes"
NOTES_PATH_PARENT_DIR = os.path.dirname(settings.BASE_DIR)
NOTES_GIT_PATH = os.path.join(NOTES_PATH_PARENT_DIR, NOTES_PATH_NAME)


def get_right_content_from_file(file_path):
    """
    读取文件时涉及到编码问题, 于是就专门写个函数来解决吧
    :param file_path: 文件路径
    :return: 文件内容, str() 形式
    """
    with open(file_path, "rb") as f:
        data = f.read()
        encoding = chardet.detect(data)["encoding"]

    try:
        data = data.decode("utf8")
    except UnicodeDecodeError:
        try:
            data = data.decode("gbk")
        except UnicodeDecodeError:
            data = data.decode(encoding)

    return data


def home(request):
    articles = Article.objects.all()  # 获取全部的Article对象
    paginator = Paginator(articles, HOME_PAGE_ARTICLES_NUMBERS)  # 每页显示 HOME_PAGE_ARTICLES_NUMBERS 篇
    page = request.GET.get('page')
    try:
        article_list = paginator.page(page)
    except PageNotAnInteger:
        article_list = paginator.page(1)
    # except EmptyPage: # 没用到, 不知道干啥的
    #     article_list = paginator.paginator(paginator.num_pages)
    return render(request, 'home.html', {'post_list': article_list, "form": ArticleForm()})


def detail(request, id):
    try:
        db_data = Article.objects.get(id=str(id))
        tags = db_data.tag.all()
    except Article.DoesNotExist:
        raise Http404
    return render(request, "article.html", {"post": db_data, "tags": tags, "form": ArticleForm()})


def archives(request):
    try:
        post_list = Article.objects.all()
    except Article.DoesNotExist:
        raise Http404
    return render(request, 'archives.html', {'post_list': post_list,
                                             'error': False, "form": ArticleForm()})


def about_me(request):
    return render(request, 'about_me.html', {"form": ArticleForm()})


def search_tag(request, tag):
    try:
        post_list = Article.objects.filter(category__iexact=tag)  # contains
    except Article.DoesNotExist:
        raise Http404
    return render(request, 'tag.html', {'post_list': post_list, "form": ArticleForm()})


def blog_search(request):
    if request.method == "POST":
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            article_list = Article.objects.filter(title__icontains=form.cleaned_data["title"])
            if len(article_list) == 0:
                return render(request, 'archives.html', {'post_list': article_list,
                                                         'error': EMPTY_ARTICLE_ERROR, "form": form})
            else:
                return render(request, 'archives.html', {'post_list': article_list,
                                                         'error': False, "form": form})
    return home(request)


def update_notes(request):
    def __get_latest_notes():
        # 进行 git 操作, 获取最新版本的笔记
        if not os.path.exists(os.path.join(NOTES_GIT_PATH, ".git")):
            command = "cd {} && git clone {} {}".format(NOTES_PATH_PARENT_DIR, TEST_GIT_REPOSITORY, NOTES_PATH_NAME)
        else:
            command = "cd {} && git reset --hard && git pull".format(NOTES_GIT_PATH)
        os.system(command)

    def __content_change(old_content, newest_content):
        """
        关于字符串比较的性能问题, 现在还没想到一个好的解决方法, 所以还是用最原始的字符串比较就是了
        :param old_content: 原来的内容
        :param newest_content: 现在的内容
        :return:
        """
        return old_content != newest_content

    def __sync_database(file_name, file_path):
        article = file_name.rstrip(".md")
        article_category, article_title = article.split("-")
        article_content = get_right_content_from_file(file_path)

        try:
            article_from_db = Article.objects.get(title=article_title)
            # 已经存在
            if __content_change(article_from_db.content, article_content):
                # 内容有所改变
                article_from_db.content = article_content
            article_from_db.category = article_category
            article_from_db.save()
        except Article.DoesNotExist:
            # 不存在
            Article.objects.create(title=article_title, category=article_category, content=article_content)

    def __is_valid_md_file(file_name):
        """
        判断文件名是否满足 测试笔记-测试标题.md 这种格式
        :param file_name: "测试笔记-测试标题.md"
        :return: True
        """
        if not file_name.endswith(".md"):
            return False
        elif "-" not in file_name:
            return False
        return True

    __get_latest_notes()

    # 将 git 仓库中的所有笔记进行更新
    notes_in_git = set()
    for root, dirs, file_list in os.walk(NOTES_GIT_PATH):
        for each_file_name in file_list:
            if __is_valid_md_file(each_file_name):
                path = os.path.join(root, each_file_name)
                __sync_database(each_file_name, path)
                notes_in_git.add(each_file_name)

    # 删除数据库中多余的笔记
    for each_note_in_db in Article.objects.all():
        note_in_db_full_name = "{}-{}.md".format(each_note_in_db.category,each_note_in_db.title)
        if note_in_db_full_name not in notes_in_git:
            each_note_in_db.delete()

    return home(request)
