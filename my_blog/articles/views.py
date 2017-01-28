# -*- coding: utf-8 -*-
# version: Python3.X
"""
2016.10.28 重构了一下模板传参, 封装成一个函数来处理了, 要不然每个视图都得专门处理传给模板的参数
"""

from django.shortcuts import render
from django.http import Http404
from django.core.paginator import Paginator, PageNotAnInteger
from django.conf import settings
from ipware.ip import get_ip, get_real_ip, get_trusted_ip

from .models import Article
from .forms import ArticleForm
from my_constant import const

import os
import chardet
import datetime
import logging
import copy

LAST_UPDATE_TIME = None

logger = logging.getLogger("my_blog.articles.views")


def get_right_content_from_file(file_path):
    """
    读取文件时涉及到编码问题, 于是就专门写个函数来解决吧
    :param file_path: 文件路径
    :return: 文件内容, str() 形式
    """
    logging.debug("读取文件内容: {}".format(file_path))
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


def get_ip_from_django_request(request):
    """
    # 用来获取访问者 IP 的
    # 参考
    ## https://my.oschina.net/u/167994/blog/156184
    ## http://stackoverflow.com/questions/4581789/how-do-i-get-user-ip-address-in-django
    :param request: 传给视图函数的 request
    :return: ip 地址, 比如 116.26.110.36
    """
    logger.debug("获取 ip 情况, get_ip:{}, get_real_ip:{}, get_trusted_ip:{}"
                 .format(get_ip(request), get_real_ip(request), get_trusted_ip(request)))
    return get_ip(request)


def __get_context_data(update_data=None):
    """
    定制要发送给模板的相关数据
    :param update_data: 以需要发送给 base.html 的数据为基础, 需要额外发送给模板的数据
    :return: dict(), 发送给模板的全部数据
    """
    data_return_to_base_template = {"form": ArticleForm(), "is_valid_click": "True",
                                    "articles_numbers": len(Article.objects.all())}
    if update_data is not None:
        data_return_to_base_template.update(update_data)

    return data_return_to_base_template


def home(request, invalid_click="True"):
    logger.info("ip: {} 访问主页了".format(get_ip_from_django_request(request)))
    articles = Article.objects.all()  # 获取全部的Article对象
    paginator = Paginator(articles, const.HOME_PAGE_ARTICLES_NUMBERS)  # 每页显示 HOME_PAGE_ARTICLES_NUMBERS 篇
    page = request.GET.get('page')
    try:
        article_list = paginator.page(page)
    except PageNotAnInteger:
        article_list = paginator.page(1)

    return render(request, 'home.html', __get_context_data({"post_list": article_list, "invalid_click": invalid_click}))


def detail(request, article_id):
    try:
        db_data = Article.objects.get(id=str(article_id))
        logger.info("ip: {} 查看文章: {}".format(get_ip_from_django_request(request), db_data.title))
        tags = db_data.tag.all()
    except Article.DoesNotExist:
        raise Http404

    return render(request, "article.html", __get_context_data({"post": db_data, "tags": tags}))


def archives(request):
    logger.info("ip: {} 查看文章列表".format(get_ip_from_django_request(request)))
    try:
        post_list = Article.objects.all()
    except Article.DoesNotExist:
        raise Http404

    return render(request, 'archives.html', __get_context_data({'post_list': post_list, 'error': False}))


def about_me(request):
    logger.info("ip: {} 查看 about me".format(get_ip_from_django_request(request)))

    return render(request, 'about_me.html', __get_context_data())


def search_tag(request, tag):
    logger.info("ip: {} 搜索 tag: {}".format(get_ip_from_django_request(request), tag))
    try:
        post_list = Article.objects.filter(category__iexact=tag)  # contains
    except Article.DoesNotExist:
        raise Http404

    return render(request, 'tag.html', __get_context_data({'post_list': post_list}))


def __create_search_result(article_list, keyword_set):
    """
    创建搜索结果以便返回给页面
    :param article_list: 存在关键词的文章列表
    :param keyword_set: set(), 每一个是一个用户搜索的关键词
    :return: list(), 每一个元素都是一个命名元组, 每一个元素的格式类似于: (id, title, content)
    """
    result_list = list()
    raw_keyword_set = copy.copy(keyword_set)

    for each_article in article_list:
        keyword_set = copy.copy(raw_keyword_set)

        result_content = str()
        # 遍历每一行, 提取出关键词所在行
        for each_line in each_article.content.splitlines():
            temp_keyword_set = set(copy.copy(keyword_set))

            # 已经搜索完所有关键词了, 就不浪费时间了
            if len(temp_keyword_set) <= 0:
                break

            for each_keyword in temp_keyword_set:
                if each_keyword.lower() in each_line.lower():
                    result_content += each_line + os.linesep
                    keyword_set.remove(each_keyword)
                    continue

        if len(result_content) <= 0:
            # 设置默认值
            result_content = const.KEYWORD_IN_TITLE

        result_list.append(const.ARTICLE_STRUCTURE(each_article.id, each_article.title, result_content))

    return result_list


def blog_search(request):
    """
    2017.01.27 重构搜索视图函数, 现在要显示搜索结果等的
    2016.10.11 添加能够搜索文章内容的功能
    :param request: django 传给视图函数的参数 request, 包含 HTTP 请求的各种信息
    :return:
    """

    def __search_keyword_in_articles(keyword_set):
        result_set = set()
        first_time = True

        # 对每个关键词进行处理
        for each_key_word in keyword_set:
            # 获取上一次过滤剩下的文章列表, 如果是第一次则为全部文章
            if first_time:
                first_time = False
                articles_from_title_filter = Article.objects.filter(title__icontains=each_key_word)
                articles_from_content_filter = Article.objects.filter(content__icontains=each_key_word)

                result_set.update(articles_from_title_filter)
                result_set.update(articles_from_content_filter)
            else:
                temp_result_set = set()
                # 对每篇文章进行查找, 先查找标题, 然后查找内容
                for each_article in result_set:
                    if each_key_word in each_article.title or each_key_word in each_article.content:
                        temp_result_set.add(each_article)

                result_set = temp_result_set

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
            keywords = set(form.data["title"].split(" "))
            # 因为自定义无视某个错误所以不能用 form.cleaned_data["title"], 详见上面这个验证函数
            article_list = __search_keyword_in_articles(keywords)
            logger.info("ip: {} 搜索: {}"
                        .format(get_ip_from_django_request(request), form.data["title"]))

            context_data = __get_context_data({'post_list': __create_search_result(article_list, keywords),
                                               'error': None, "form": form})
            context_data["error"] = const.EMPTY_ARTICLE_ERROR if len(article_list) == 0 else False

            return render(request, 'search_result.html', context_data)

    return home(request)


def update_notes(request=None):
    def __get_latest_notes():
        nonlocal notes_git_path

        # 进行 git 操作, 获取最新版本的笔记
        if not os.path.exists(os.path.join(notes_git_path, ".git")):
            command = ("cd {} && git clone {} {}"
                       .format(const.NOTES_PATH_PARENT_DIR, const.ARTICLES_GIT_REPOSITORY, const.NOTES_PATH_NAME))
        else:
            command = "cd {} && git reset --hard && git pull".format(notes_git_path)
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
                article_from_db.update_time = datetime.datetime.now()
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

    notes_git_path = const.NOTES_GIT_PATH

    if request:
        logger.info("ip: {} 更新了笔记".format(get_ip_from_django_request(request)))

    # settings.UPDATE_TIME_LIMIT s 内不允许重新点击
    global LAST_UPDATE_TIME
    now = datetime.datetime.today()
    if LAST_UPDATE_TIME is not None and (now - LAST_UPDATE_TIME).total_seconds() < settings.UPDATE_TIME_LIMIT:
        return home(request, "invalid_click") if request is not None else None
    else:
        LAST_UPDATE_TIME = now

    # 将 git 仓库中的所有笔记更新到本地
    __get_latest_notes()

    # 将从 git 中获取到本地的笔记更新到数据库中
    notes_in_git = set()
    for root, dirs, file_list in os.walk(notes_git_path):
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

    return home(request) if request is not None else None
