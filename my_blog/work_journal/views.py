from django.shortcuts import render
from .models import Journal
from .forms import JournalForm


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
