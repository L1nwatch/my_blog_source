# 标准库
from django.shortcuts import render

# 自己的模块
import my_constant as const


def travel_event_timeline(request):
    """
    负责记录 travel 时间的 timeline 视图函数
    :param request: Django 的 request 对象
    :return: 渲染过后的 html
    """
    return render(request, const.TRAVEL_EVENT_TIMELINE_TEMPLATE)
