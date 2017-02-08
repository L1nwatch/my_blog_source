from django.shortcuts import render
from .models import Journal
from .forms import JournalForm
from my_constant import const
from articles.views import get_ip_from_django_request, get_right_content_from_file, create_search_result

import re
import logging
import datetime
import os

logger = logging.getLogger("my_blog.work_journal.views")


def _get_context_data(update_data=None):
    """
    定制要发送给模板的相关数据
    :param update_data: 以需要发送给 base.html 的数据为基础, 需要额外发送给模板的数据
    :return: dict(), 发送给模板的全部数据
    """
    data_return_to_base_template = {"form": JournalForm(), "is_valid_click": "True",
                                    "journals_numbers": len(Journal.objects.all())}
    if update_data is not None:
        data_return_to_base_template.update(update_data)

    return data_return_to_base_template


def work_journal_home_view(request):
    journal_list = Journal.objects.all()  # 获取全部的 Journal 对象
    return render(request, 'journal_home.html', _get_context_data({"post_list": journal_list}))


def journal_display(request, journal_id):
    """
    :param request: 发送给视图函数的请求
    :param journal_id: 请求的日记 id
    """
    journal = Journal.objects.get(id=journal_id)
    return render(request, 'journal_display.html', _get_context_data({"post": journal}))


def is_valid_update_md_file(file_name):
    """
    判断文件名是否满足 2017-02-03-任务情况总结.md 这种格式
    :param file_name: str(), 比如 "2017-02-03-任务情况总结.md"
    :return: True
    """
    if not file_name.endswith(".md"):
        return False
    elif not re.match("\d+-?\d+-?\d+-?.*\.md", file_name):
        return False
    return True


def extract_date_from_md_file(file_name):
    """
    从文件名提取出 date 对象, 用于创建日记用的
    :param file_name: str(), 比如 "2017-02-03-任务情况总结.md"
    :return: date(), 比如利用 2017-02-03 生成的 date 对象
    """
    result = re.findall("(\d{4})-?(\d{1,2})-?(\d{1,2})-?.*", file_name)[0]
    year, month, day = int(result[0]), int(result[1]), int(result[2])
    return datetime.date(year, month, day)


def update_journals(request=None):
    def __get_latest_notes():
        nonlocal notes_git_path

        # 进行 git 操作, 获取最新版本的笔记
        if not os.path.exists(os.path.join(notes_git_path, ".git")):
            command = ("cd {} && git clone {} {}"
                       .format(const.NOTES_PATH_PARENT_DIR, const.JOURNALS_GIT_REPOSITORY, const.JOURNALS_PATH_NAME))
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
        journal_title = file_name.rstrip(".md")
        journal_content = get_right_content_from_file(file_path)

        try:
            journal_from_db = Journal.objects.get(title=journal_title)
            # 已经存在
            if __content_change(journal_from_db.content, journal_content):
                # 内容被清空了
                if journal_content == "":
                    # 删除原来那篇文章
                    journal_from_db.delete()
                else:
                    # 内容有所改变
                    journal_from_db.content = journal_content
                    journal_from_db.save()
        except Journal.DoesNotExist:
            # 不存在并且不为空
            if journal_content != "":
                date = extract_date_from_md_file(journal_title)
                Journal.objects.create(title=journal_title, content=journal_content, date=date)

    notes_git_path = const.JOURNALS_GIT_PATH

    if request:
        logger.info("ip: {} 于时间 {} 更新了笔记".format(get_ip_from_django_request(request), datetime.datetime.today()))

    # 将 git 仓库中的所有笔记更新到本地
    __get_latest_notes()

    # 将从 git 中获取到本地的笔记更新到数据库中
    notes_in_git = set()
    for root, dirs, file_list in os.walk(notes_git_path):
        for each_file_name in file_list:
            if is_valid_update_md_file(each_file_name):
                path = os.path.join(root, each_file_name)
                __sync_database(each_file_name, path)
                notes_in_git.add(each_file_name)

    # 删除数据库中多余的笔记
    for each_note_in_db in Journal.objects.all():
        note_in_db_full_name = "{}.md".format(each_note_in_db.title)
        if note_in_db_full_name not in notes_in_git:
            each_note_in_db.delete()

    return work_journal_home_view(request) if request is not None else None


def search_journals(request):
    """
    2017.02.08 参考搜索文章的代码, 写了这个搜索日记的代码
    :param request: django 传给视图函数的参数 request, 包含 HTTP 请求的各种信息
    """

    def __search_keyword_in_articles(keyword_set):
        result_set = set()
        first_time = True

        # 对每个关键词进行处理
        for each_key_word in keyword_set:
            # 获取上一次过滤剩下的文章列表, 如果是第一次则为全部文章
            if first_time:
                first_time = False
                articles_from_content_filter = Journal.objects.filter(content__icontains=each_key_word)

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
        :param my_form: form = JournalForm(data=request.POST)
        :return: boolean, True or False
        """
        if my_form.is_valid() is True:
            return True
        elif len(my_form.errors) == 1 and "具有 Title 的 Article 已存在。" in str(my_form.errors):
            return True
        return False

    if request.method == "POST":
        form = JournalForm(data=request.POST)
        if __form_is_valid_and_ignore_exist_article_error(form):
            keywords = set(form.data["title"].split(" "))
            # 因为自定义无视某个错误所以不能用 form.cleaned_data["title"], 详见上面这个验证函数
            article_list = __search_keyword_in_articles(keywords)
            logger.info("ip: {} 搜索: {}"
                        .format(get_ip_from_django_request(request), form.data["title"]))

            context_data = _get_context_data({'post_list': create_search_result(article_list, keywords),
                                              'error': None, "form": form})
            context_data["error"] = const.EMPTY_ARTICLE_ERROR if len(article_list) == 0 else False

            return render(request, 'search_result.html', context_data)

    return work_journal_home_view(request)
