#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.03.22 添加有关备选菜单的相关代码实线
2017.03.10 将记录日记的装饰器装饰到对应视图上
"""
from django.http import Http404
from django.shortcuts import render

from articles.common_help_function import log_wrapper
from my_constant import const

import logging

logger = logging.getLogger("my_blog.just_eating.views")

school_backup_list = ["美食坊快餐",
                      "丁香快餐",
                      "海棠快餐",
                      "小米鸡排饭",
                      "微辣香锅",
                      "川味-香干肉丝",
                      "川渝-腐竹炒肉"]


def create_home_menu():
    home_menu = list()

    monday = const.EATING_MENU_STRUCTURE("周一", "-", "-", "牛肉盖饭\n冬瓜汤")
    tuesday = const.EATING_MENU_STRUCTURE("周二", "-", "-", "白菜炒腐竹\n紫菜鱼丸汤")
    wednesday = const.EATING_MENU_STRUCTURE("周三", "-", "-", "盒饭")
    thursday = const.EATING_MENU_STRUCTURE("周四", "-", "-", "手抓饼")
    friday = const.EATING_MENU_STRUCTURE("周五", "-", "-", "牛肉炒粿条\n汤")
    saturday = const.EATING_MENU_STRUCTURE("周六", "-", "-", "-")
    sunday = const.EATING_MENU_STRUCTURE("周日", "-", "-",
                                         ("可乐鸡翅?href=http://www.xinshipu.com/zuofa/227911\n"
                                          "豆芽炒油豆腐?href=http://www.xinshipu.com/zuofa/116954"))

    for each_day in [monday, tuesday, wednesday, thursday, friday, saturday, sunday]:
        home_menu.append(each_day)

    return home_menu


def create_school_menu():
    school_menu = list()

    monday = const.EATING_MENU_STRUCTURE("周一", "丁香\n杂粮煎饼\n豆浆", "新综\n香干炒肉(油!)", "竹园\n蒙古烤肉(油!)")
    tuesday = const.EATING_MENU_STRUCTURE("周二", "海棠\n照烧鸡腿饼", "海棠\n川渝-杏鲍菇炒肉", "竹园\n快餐")
    wednesday = const.EATING_MENU_STRUCTURE("周三", "竹园\n手抓饼\n牛奶", "海棠\n川味椒盐里脊", "新综\n黑椒牛柳")
    thursday = const.EATING_MENU_STRUCTURE("周四", "海棠\n杂粮煎饼", "丁香\n农家小炒肉", "新综\n快餐")
    friday = const.EATING_MENU_STRUCTURE("周五", "海棠\n花干菜夹馍\n豆浆", "待定", "丁香\n三楼自选快餐")
    saturday = const.EATING_MENU_STRUCTURE("周六", "老综\n卤肉卷or土豆片夹馍\n", "待定", " 新综\n包菜肉片(油!)")
    sunday = const.EATING_MENU_STRUCTURE("周日", "新综+海棠\n安仔包\n俩鸡肉+豆浆", "新综\n鸡米花饭", "待定")

    for each_day in [monday, tuesday, wednesday, thursday, friday, saturday, sunday]:
        school_menu.append(each_day)

    return school_menu


@log_wrapper(str_format="查看了菜单", logger=logger)
def just_eating_home_view(request, eating_place):
    eating_times = ["", "早餐", "午餐", "晚餐"]

    if eating_place == "" or eating_place == "home":
        menu = create_home_menu()
        eating_place_name = "Home"
    elif eating_place == "school":
        menu = create_school_menu()
        eating_place_name = "School"
    else:
        raise Http404
    return render(request, "just_eating_base.html", {"eating_days": menu,
                                                     "eating_times": eating_times,
                                                     "eating_place": eating_place_name})


@log_wrapper(str_format="使用了随机选择食物的功能", logger=logger)
def random_eating(request, eating_place):
    return render(request, "just_eating_spinner.html", {"food_list": school_backup_list})
