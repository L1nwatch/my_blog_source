# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.12.03 优化判断合法 IP 的方式
2017.08.26 给日记加上 IP 访问限制
2017.06.17 将搜索 Tag 的视图函数进行扩展, 使其能够支持 GitBook 的 Tag 搜索
2017.06.08 更改 tag/category 采用和 archives 一样的界面
2017.06.06 实现基于 tag 的搜索
2017.06.04 更新笔记时现在会添加 Tag 了
2017.05.21 实现搜索结果按照点击次数排序的相关视图代码
2017.05.21 日志记录的格式有问题, 修正一下
2017.05.01 完善一下验证更新时间的前台交互代码
2017.03.30 给更新函数添加记日记功能
2017.03.28 新增有关 Code 的搜索实现
2017.03.26 新增搜索时拒绝非法字符搜索的相关功能
2017.03.25 修正一下更新笔记时会删除过多后缀的问题, 重新改了一下搜索排序
2017.03.23 增加有关搜索结果按关键词出现次数排序的相关代码
2017.03.23 重构了部分搜索实现, 删除了通过 URL 来区分搜索类型的相关代码
2017.03.18 修正一下解析 markdown tree 的问题, 原本以为是 md 不友好, 结果是自己的代码有问题。。。
2017.03.17 遇到了 markdown tree 解析的问题, 修正一下
2017.03.16 重构了搜索框, 于是搜索类型不再是通过 url 传递的了
2017.03.08 进行重构
2017.03.07 新增 form data 的清理工作
2017.03.05 添加 GitBook 的搜索
2017.02.09 重构一下搜索函数, 跟日记搜索的功能合并一下
2016.10.28 重构了一下模板传参, 封装成一个函数来处理了, 要不然每个视图都得专门处理传给模板的参数
"""
# 标准库
import datetime
import logging
import os
import re
import traceback

import md2py
from django.conf import settings
from django.http import Http404
from django.shortcuts import render, redirect, HttpResponse

# 自己的模块
from articles.forms import ArticleForm, BaseSearchForm
from articles.models import Article, Tag
from articles.templatetags.custom_filter import custom_markdown_for_tree_parse
from code_collect.views import do_code_search
from common_module.common_help_function import (clean_form_data, search_keyword_in_model,
                                                create_search_result, get_right_content_from_file, get_context_data,
                                                form_is_valid_and_ignore_exist_error, log_wrapper, sort_search_result,
                                                extract_tag_name_from_path, get_ip_from_django_request, is_valid_ip)
from gitbook_notes.views import do_gitbooks_search
import my_constant as const
from work_journal.views import do_journals_search

LAST_UPDATE_TIME = None

logger = logging.getLogger("my_blog.articles.views")


@log_wrapper(str_format="尝试进行更新操作", level="info", logger=logger)
def update_note_check_view(request):
    """
    用于前台判断是否现在可以执行更新操作
    """
    if request.method == "GET":
        if is_valid_time_to_update():
            return HttpResponse("Yes")
        else:
            return HttpResponse("No")
    return HttpResponse("[-] Please Use GET Method")


def is_valid_time_to_update():
    """
    判断现在是否可以进行更新操作
    """
    global LAST_UPDATE_TIME
    now = datetime.datetime.today()
    if LAST_UPDATE_TIME is not None and (now - LAST_UPDATE_TIME).total_seconds() < settings.UPDATE_TIME_LIMIT:
        return False
    return True


@log_wrapper(str_format="访问主页", logger=logger)
def home_view(request):
    return render(request, 'new_home.html', get_context_data(request, "all"))


@log_wrapper(str_format="进行了 Google 站长认证", logger=logger)
def google_verify(request):
    return render(request, "googlef0b96351a9e6fd45.html")


@log_wrapper(str_format="查看文章", logger=logger)
def article_display(request, article_id):
    """
    负责显示文章的视图函数
    2017.01.30 添加 markdown 树的解析结果
    :param request: django 传给视图函数的参数 request, 包含 HTTP 请求的各种信息
    :param article_id: 文章 id 号
    """
    try:
        db_data = Article.objects.get(id=str(article_id))
        tags = db_data.tag.all()
        toc_data = _parse_markdown_file(db_data.content)
    except Article.DoesNotExist:
        raise Http404

    if request.method == "POST" and request.POST["visited"] == "True":
        db_data.click_times += 1
        db_data.save()

    return render(request, "article.html",
                  get_context_data(request, "articles",
                                   update_data={"post": db_data, "tags": tags, "toc": toc_data}
                                   )
                  )


def _get_id_from_markdown_html(markdown_html, tag_content):
    """
    从 markdown html 中获取对应标题的 id 信息
    :param markdown_html: str(), 比如 '<h1 id="_1">一级标题</h1>'
    :param tag_content: str(), 比如 "一级标题"
    :return: 查找成功则返回 str(), "_1", 即 id 信息
    """
    result = re.findall('<h\d id="(.*)">{}</h\d>'.format(re.escape(tag_content)), markdown_html)
    if len(result) > 0:
        result = result[0]
        return result


@log_wrapper(str_format="查看文章列表", logger=logger)
def archives_view(request):
    try:
        post_list = Article.objects.all()
    except Article.DoesNotExist:
        raise Http404

    return render(request, 'archives.html',
                  get_context_data(request, "articles", update_data={'post_list': post_list, 'error': False})
                  )


@log_wrapper(str_format="查看 About Me", logger=logger)
def about_me_view(request):
    return render(request, 'about_me.html', get_context_data(request, "all"))


@log_wrapper(str_format="查看 About Me 英文版", logger=logger)
def about_me_en_view(request):
    return render(request, 'about_me_en.html', get_context_data(request, "all"))


@log_wrapper(str_format="进行了 Category 搜索", logger=logger)
def search_category_view(request, category):
    try:
        post_list = Article.objects.filter(category__iexact=category)  # contains
    except Article.DoesNotExist:
        raise Http404

    return render(request, const.CATEGORY_TEMPLATE, get_context_data(request, "articles", {'post_list': post_list}))


def _parse_markdown_file(markdown_content):
    def __recursive_create(root, current_tag_level):
        """
        递归创建结果数组
        2017.03.18 避免递归到最后一级 h6 时报错
        :param root: 当前树的根节点
        :param current_tag_level: str(), 比如 "h1", 表示从这一级开始往下递归
        :return: list(), 结果数组
        """
        next_tag_dict = {"h1": "h2", "h2": "h3", "h3": "h4", "h4": "h5", "h5": "h6", "h6": None}

        if root and current_tag_level:
            result = list()

            if root.__getattr__(current_tag_level) is not None:
                for each_h in root.__getattr__("{}s".format(current_tag_level)):
                    result.append(
                        const.MARKDOWN_TREE_STRUCTURE(str(each_h),
                                                      _get_id_from_markdown_html(str(each_h.source), str(each_h)),
                                                      __recursive_create(each_h, next_tag_dict[current_tag_level]))
                    )

            if len(result) <= 0:
                result = None

            return result

    def __get_root_title(toc_tree):
        """
        获取顶级标题
        :param toc_tree: toc 树
        :return: str(), 比如 "h1", 表示顶级标题为一级标题
        """
        for each_level in ["h1", "h2", "h3", "h4", "h5", "h6"]:
            # 找到顶级标题了
            if toc_tree.__getattr__(each_level) is not None:
                return each_level

    markdown_content_length = len(markdown_content)
    display_length = markdown_content_length if markdown_content_length < 200 else 200
    try:
        if markdown_content_length > 0:
            toc = md2py.TreeOfContents.fromHTML(custom_markdown_for_tree_parse(markdown_content))
            root_level = __get_root_title(toc)
            if root_level:
                result_list = __recursive_create(toc, root_level)
                return result_list
    except TypeError:
        logging.error("[-] 解析 Markdown 出错, 针对内容: {}".format(markdown_content[:display_length]))
    except Exception as e:
        traceback.print_exc()
        logging.error("[-] 解析 Markdown 出错, 针对内容: {}".format(markdown_content[:display_length]))


@log_wrapper(str_format="进行了搜索", logger=logger)
def do_articles_search(request):
    """
    2017.03.26 删除验证 form 的代码, 在上一层已经验证过了
    2017.02.09 分离搜索视图, 将搜索文章的单独拿出来
    :param request: django 传给视图函数的参数 request, 包含 HTTP 请求的各种信息
    :return: dict() or None, 要传给模板的各个数据, None 表示出现异常了
    """
    form = ArticleForm(data=request.POST)
    keywords = set(clean_form_data(form.data["search_content"]).split(" "))
    # 因为自定义无视某个错误所以不能用 form.cleaned_data["title"], 详见上面这个验证函数
    article_list = search_keyword_in_model(keywords, Article, ["content", "title"])

    context_data = get_context_data(request, "articles",
                                    {'post_list': create_search_result(article_list, keywords, "articles"),
                                     'error': None, "form": form})
    context_data["error"] = const.EMPTY_ARTICLE_ERROR if len(article_list) == 0 else False

    return context_data


@log_wrapper(str_format="进行了搜索", logger=logger)
def blog_search(request):
    """
    2017.03.16 重构了搜索框, 于是搜索类型不再是通过 url 传递的了
    2017.02.18 实现日记和文章同时搜索的功能
    2017.02.08 要重构视图搜索函数, 支持搜索指定类型的数据, 比如说只搜索文章, 只搜索日记等
    2017.01.27 重构搜索视图函数, 现在要显示搜索结果等的
    2016.10.11 添加能够搜索文章内容的功能
    :param request: django 传给视图函数的参数 request, 包含 HTTP 请求的各种信息
    """
    if request.method == "POST" and form_is_valid_and_ignore_exist_error(BaseSearchForm(request.POST)):
        context_data = None
        if request.POST["search_choice"] == "all":
            context_data = get_context_data(request, "all", {"total_numbers": 0})

            article_search_result = do_articles_search(request)
            if article_search_result is not None:
                context_data["total_numbers"] += article_search_result["articles_numbers"]
                context_data["post_list"] = context_data.get("post_list", list()) + article_search_result["post_list"]

            # 仅限本地访问
            if is_valid_ip(get_ip_from_django_request(request)):
                journal_search_result = do_journals_search(request)
                if journal_search_result is not None:
                    context_data["total_numbers"] += journal_search_result["journals_numbers"]
                    context_data["post_list"] = context_data.get("post_list", list()) + journal_search_result[
                        "post_list"]

            gitbooks_search_result = do_gitbooks_search(request)
            if gitbooks_search_result is not None:
                context_data["total_numbers"] += gitbooks_search_result["gitbooks_numbers"]
                context_data["post_list"] = context_data.get("post_list", list()) + gitbooks_search_result["post_list"]

            if not context_data.get("post_list", list()):
                context_data["error"] = const.EMPTY_ARTICLE_ERROR

        elif request.POST["search_choice"] == "articles":
            context_data = do_articles_search(request)
        elif request.POST["search_choice"] == "journals" and is_valid_ip(get_ip_from_django_request(request)):
            context_data = do_journals_search(request)
        elif request.POST["search_choice"] == "gitbooks":
            context_data = do_gitbooks_search(request)
        elif request.POST["search_choice"] == "code":
            context_data = do_code_search(request)

        if context_data is not None and len(context_data) > 0:
            context_data["post_list"] = sort_search_result(context_data["post_list"])
            return render(request, 'search_result.html', context_data)

    return redirect("home")


@log_wrapper(str_format="更新了笔记", logger=logger)
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
        nonlocal notes_git_path
        article = file_name[:-len(".md")]  # 用 rstrip 会删除多余后缀
        article_category, article_title = article.split("-")
        article_content = get_right_content_from_file(file_path)
        tag_names = extract_tag_name_from_path(notes_git_path, file_path)

        try:
            article_from_db = Article.objects.get(title=article_title)
            # 已经存在
            if __content_change(article_from_db.content, article_content):
                # 内容有所改变
                article_from_db.content = article_content
                article_from_db.update_time = datetime.datetime.now()
            article_from_db.category = article_category
            article_from_db.save()
            article = article_from_db
        except Article.DoesNotExist:
            # 不存在
            article = Article.objects.create(title=article_title, category=article_category, content=article_content)

        article.tag = [(Tag.objects.get_or_create(tag_name=x))[0] for x in tag_names]

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

    # settings.UPDATE_TIME_LIMIT s 内不允许重新点击
    if is_valid_time_to_update():
        global LAST_UPDATE_TIME
        LAST_UPDATE_TIME = datetime.datetime.today()
    else:
        return home_view(request) if request is not None else None

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

    return archives_view(request) if request is not None else None
