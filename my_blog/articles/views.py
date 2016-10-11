#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X

from django.shortcuts import render
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

from .models import Article
from .forms import ArticleForm, EMPTY_ARTICLE_ERROR

import os
import chardet
import datetime

HOME_PAGE_ARTICLES_NUMBERS = 2
TEST_GIT_REPOSITORY = settings.TEST_GIT_REPOSITORY
NOTES_PATH_NAME = "notes"
NOTES_PATH_PARENT_DIR = os.path.dirname(settings.BASE_DIR)
NOTES_GIT_PATH = os.path.join(NOTES_PATH_PARENT_DIR, NOTES_PATH_NAME)
LAST_UPDATE_TIME = None


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


def home(request, valid_click="True"):
    articles = Article.objects.all()  # 获取全部的Article对象
    paginator = Paginator(articles, HOME_PAGE_ARTICLES_NUMBERS)  # 每页显示 HOME_PAGE_ARTICLES_NUMBERS 篇
    page = request.GET.get('page')
    try:
        article_list = paginator.page(page)
    except PageNotAnInteger:
        article_list = paginator.page(1)
    # except EmptyPage: # 没用到, 不知道干啥的
    #     article_list = paginator.paginator(paginator.num_pages)
    return render(request, 'home.html',
                  {'post_list': article_list, "form": ArticleForm(), "is_valid_click": valid_click})


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
    """
    2016.10.11 添加能够搜索文章内容的功能
    :param request: django 传给视图函数的参数 request, 包含 HTTP 请求的各种信息
    :return:
    """

    def __search_keyword_in_articles(keyword):
        key_word_list = keyword.split(" ")
        result_set = set()
        articles_from_title_filter, articles_from_content_filter = list(), list()

        for each_key_word in key_word_list:
            articles_from_title_filter.append(set(Article.objects.filter(title__icontains=each_key_word)))
            articles_from_content_filter.append(set(Article.objects.filter(content__icontains=each_key_word)))
        if len(articles_from_title_filter) > 0:
            result_set.update(set.intersection(*articles_from_title_filter))
        if len(articles_from_content_filter) > 0:
            result_set.update(set.intersection(*articles_from_content_filter))
        return result_set

    def __form_is_valid_and_ignore_exist_article_error(my_form):
        """
        2016.10.11 重定义验证函数, 不再使用简单的 form.is_valid, 原因是执行搜索的时候发现不能搜索跟已存在的文章一模一样的标题关键词
        :param my_form: form = ArticleForm(data=request.POST)
        :return:
        """
        if my_form.is_valid() is True:
            return True
        elif len(my_form.errors) == 1 and "具有 Title 的 Article 已存在。" in str(my_form.errors):
            return True
        return False

    if request.method == "POST":
        form = ArticleForm(data=request.POST)
        if __form_is_valid_and_ignore_exist_article_error(form):
            # 因为自定义无视某个错误所以不能用 form.cleaned_data["title"], 详见上面这个验证函数
            article_list = __search_keyword_in_articles(form.data["title"])

            data_return_to_template = {'post_list': article_list, 'error': None, "form": form}
            if len(article_list) == 0:
                data_return_to_template["error"] = EMPTY_ARTICLE_ERROR
            else:
                data_return_to_template["error"] = False
            return render(request, 'archives.html', data_return_to_template)

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

    # settings.UPDATE_TIME_LIMIT s 内不允许重新点击
    global LAST_UPDATE_TIME
    now = datetime.datetime.today()
    if LAST_UPDATE_TIME is not None and (now - LAST_UPDATE_TIME).total_seconds() < settings.UPDATE_TIME_LIMIT:
        return home(request, "invalid_click")
    else:
        LAST_UPDATE_TIME = now

    # 将 git 仓库中的所有笔记更新到本地
    __get_latest_notes()

    # 将从 git 中获取到本地的笔记更新到数据库中
    notes_in_git = set()
    for root, dirs, file_list in os.walk(NOTES_GIT_PATH):
        for each_file_name in file_list:
            if __is_valid_md_file(each_file_name):
                path = os.path.join(root, each_file_name)
                __sync_database(each_file_name, path)
                notes_in_git.add(each_file_name)

    # 删除数据库中多余的笔记
    for each_note_in_db in Article.objects.all():
        note_in_db_full_name = "{}-{}.md".format(each_note_in_db.category, each_note_in_db.title)
        if note_in_db_full_name not in notes_in_git:
            each_note_in_db.delete()

    return home(request)
