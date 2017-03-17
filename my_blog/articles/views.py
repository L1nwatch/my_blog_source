# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.03.17 遇到了 markdown tree 解析的问题, 修正一下
2017.03.16 重构了搜索框, 于是搜索类型不再是通过 url 传递的了
2017.03.08 进行重构
2017.03.07 新增 form data 的清理工作
2017.03.05 添加 GitBook 的搜索
2017.02.09 重构一下搜索函数, 跟日记搜索的功能合并一下
2016.10.28 重构了一下模板传参, 封装成一个函数来处理了, 要不然每个视图都得专门处理传给模板的参数
"""
from django.shortcuts import render
from django.http import Http404
from django.conf import settings

from articles.models import Article
from articles.forms import ArticleForm
from articles.templatetags.custom_filter import custom_markdown_for_tree_parse
from articles.common_help_function import (clean_form_data, get_ip_from_django_request, search_keyword_in_model,
                                           create_search_result, get_right_content_from_file, get_context_data,
                                           form_is_valid_and_ignore_exist_error, log_wrapper)
from my_constant import const
from work_journal.views import do_journals_search
from gitbook_notes.views import do_gitbooks_search

import md2py
import datetime
import traceback
import re
import os
import logging

LAST_UPDATE_TIME = None

logger = logging.getLogger("my_blog.articles.views")


@log_wrapper(str_format="访问主页", logger=logger)
def home_view(request):
    return render(request, 'new_home.html', get_context_data(request, "all"))


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


@log_wrapper(str_format="进行了搜索", logger=logger)
def search_tag_view(request, tag):
    try:
        post_list = Article.objects.filter(category__iexact=tag)  # contains
    except Article.DoesNotExist:
        raise Http404

    return render(request, 'tag.html', get_context_data(request, "articles", {'post_list': post_list}))


def _parse_markdown_file(markdown_content):
    def __recursive_create(root, current_tag_level):
        """
        递归创建结果数组
        :param root: 当前树的根节点
        :param current_tag_level: str(), 比如 "h1", 表示从这一级开始往下递归
        :return: list(), 结果数组
        """
        next_tag_dict = {"h1": "h2", "h2": "h3", "h3": "h4", "h4": "h5", "h5": "h6"}

        if root:
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
        logging.error("[- 解析 Markdown 出错, 针对内容: {}".format(markdown_content[:display_length]))
    except Exception as e:
        traceback.print_exc()
        logging.error("[-] 解析 Markdown 出错, 针对内容: {}".format(markdown_content[:display_length]))


@log_wrapper(str_format="进行了搜索", logger=logger)
def do_articles_search(request):
    """
    2017.02.09 分离搜索视图, 将搜索文章的单独拿出来
    :param request: django 传给视图函数的参数 request, 包含 HTTP 请求的各种信息
    :return: dict() or None, 要传给模板的各个数据, None 表示出现异常了
    """

    form = ArticleForm(data=request.POST)
    if form_is_valid_and_ignore_exist_error(form):
        keywords = set(clean_form_data(form.data["search_content"]).split(" "))
        # 因为自定义无视某个错误所以不能用 form.cleaned_data["title"], 详见上面这个验证函数
        article_list = search_keyword_in_model(keywords, Article, ["content", "title"])

        context_data = get_context_data(request, "articles",
                                        {'post_list': create_search_result(article_list, keywords, "articles"),
                                         'error': None, "form": form})
        context_data["error"] = const.EMPTY_ARTICLE_ERROR if len(article_list) == 0 else False

        return context_data


@log_wrapper(str_format="进行了搜索", logger=logger)
def blog_search(request, search_type="all"):
    """
    2017.03.16 重构了搜索框, 于是搜索类型不再是通过 url 传递的了
    2017.02.18 实现日记和文章同时搜索的功能
    2017.02.08 要重构视图搜索函数, 支持搜索指定类型的数据, 比如说只搜索文章, 只搜索日记等
    2017.01.27 重构搜索视图函数, 现在要显示搜索结果等的
    2016.10.11 添加能够搜索文章内容的功能
    :param search_type: str(), 指定要搜索哪部分内容, 比如 "all" 表示全部, "articles" 表示只搜文章, "journals" 表示只搜日记
    :param request: django 传给视图函数的参数 request, 包含 HTTP 请求的各种信息
    """
    if request.method == "POST":
        context_data = None
        if request.POST["search_choice"] == "all":
            context_data = get_context_data(request, "all", {"total_numbers": 0})

            article_search_result = do_articles_search(request)
            if article_search_result is not None:
                context_data["total_numbers"] += article_search_result["articles_numbers"]
                context_data["post_list"] = context_data.get("post_list", list()) + article_search_result["post_list"]

            journal_search_result = do_journals_search(request)
            if journal_search_result is not None:
                context_data["total_numbers"] += journal_search_result["journals_numbers"]
                context_data["post_list"] = context_data.get("post_list", list()) + journal_search_result["post_list"]

            gitbooks_search_result = do_gitbooks_search(request)
            if gitbooks_search_result is not None:
                context_data["total_numbers"] += gitbooks_search_result["gitbooks_numbers"]
                context_data["post_list"] = context_data.get("post_list", list()) + gitbooks_search_result["post_list"]

            if not context_data.get("post_list", list()):
                context_data["error"] = const.EMPTY_ARTICLE_ERROR

        elif request.POST["search_choice"] == "articles":
            context_data = do_articles_search(request)
        elif request.POST["search_choice"] == "journals":
            context_data = do_journals_search(request)
        elif request.POST["search_choice"] == "gitbooks":
            context_data = do_gitbooks_search(request)

        if context_data is not None and len(context_data) > 0:
            return render(request, 'search_result.html', context_data)

    return home_view(request)


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
        # TODO: 这里只是前台的判断无效了, 后台还是有判断的
        return home_view(request) if request is not None else None
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

    return archives_view(request) if request is not None else None
