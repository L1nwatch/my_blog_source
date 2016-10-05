from django.shortcuts import render, redirect
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

from .models import Article

import os
import chardet
import locale
import sys

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
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    # except EmptyPage: # 没用到, 不知道干啥的
    #     post_list = paginator.paginator(paginator.num_pages)
    return render(request, 'home.html', {'post_list': post_list})


def detail(request, id):
    try:
        db_data = Article.objects.get(id=str(id))
        tags = db_data.tag.all()
    except Article.DoesNotExist:
        raise Http404
    return render(request, "article.html", {"post": db_data, "tags": tags})


def archives(request):
    try:
        post_list = Article.objects.all()
    except Article.DoesNotExist:
        raise Http404
    return render(request, 'archives.html', {'post_list': post_list,
                                             'error': False})


def about_me(request):
    return render(request, 'about_me.html')


def search_tag(request, tag):
    try:
        post_list = Article.objects.filter(category__iexact=tag)  # contains
    except Article.DoesNotExist:
        raise Http404
    return render(request, 'tag.html', {'post_list': post_list})


def blog_search(request):
    if 's' in request.GET:
        s = request.GET['s']
        if not s:
            return render(request, 'home.html')
        else:
            post_list = Article.objects.filter(title__icontains=s)
            if len(post_list) == 0:
                return render(request, 'archives.html', {'post_list': post_list,
                                                         'error': True})
            else:
                return render(request, 'archives.html', {'post_list': post_list,
                                                         'error': False})
    return redirect('/')


def __get_latest_notes():
    # 进行 git 操作, 获取最新版本的笔记
    if not os.path.exists(os.path.join(NOTES_GIT_PATH, ".git")):
        command = "cd {} && git clone {} {}".format(NOTES_PATH_PARENT_DIR, TEST_GIT_REPOSITORY, NOTES_PATH_NAME)
    else:
        command = "cd {} && git reset --hard && git pull".format(NOTES_GIT_PATH)
    os.system(command)


def __is_valid_md_file(file_name):
    """
    判断文件名是否满足 测试笔记-测试标题.md 这种格式
    :param file_name: "测试笔记-测试标题.md"
    :return: True
    """
    if file_name.endswith(".md") and "-" in file_name:
        return True
    return False


def update_notes(request):
    locale.setlocale(locale.LC_ALL, "zh_CN.utf8")

    __get_latest_notes()

    for root, dirs, file_list in os.walk(NOTES_GIT_PATH):
        for each_file in file_list:
            if __is_valid_md_file(each_file):
                article = each_file.rstrip(".md")
                article_category, article_title = article.split("-")
                file_path = os.path.join(root, each_file)
                article_content = get_right_content_from_file(file_path)
                with open("../../my_log.log", "w") as f:
                    print(locale.getlocale(), file=f)
                    print("1", file=f)
                    print(sys.getdefaultencoding(), file=f)
                    print("test path={}".format(file_path), file=f)
                    print("正在测试文件: {}, 文件内容为: {}".format(file_path, article_content[:100]), file=f)

                try:
                    article_from_db = Article.objects.get(title=article_title)
                    # 已经存在
                    article_from_db.content = article_content
                    article_from_db.category = article_category
                    article_from_db.save()
                except Article.DoesNotExist:
                    # 不存在
                    Article.objects.create(title=article_title, category=article_category, content=article_content)

    return redirect("/")
