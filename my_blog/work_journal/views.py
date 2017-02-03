from django.shortcuts import render
from django.http import Http404
from .models import Journal
from .forms import JournalForm
from my_constant import const
from articles.views import get_ip_from_django_request, get_right_content_from_file

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
                # 内容有所改变
                journal_from_db.content = journal_content
                journal_from_db.update_time = datetime.datetime.now()
            journal_from_db.save()
        except Journal.DoesNotExist:
            # 不存在
            Journal.objects.create(title=journal_title, content=journal_content)

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

    notes_git_path = const.JOURNALS_GIT_PATH

    if request:
        logger.info("ip: {} 于时间 {} 更新了笔记".format(get_ip_from_django_request(request), datetime.datetime.today()))

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
        for each_note_in_db in Journal.objects.all():
            note_in_db_full_name = "{}.md".format(each_note_in_db.title)
            if note_in_db_full_name not in notes_in_git:
                each_note_in_db.delete()

    return work_journal_home_view(request) if request is not None else None
