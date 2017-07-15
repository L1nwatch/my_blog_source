#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.06.24 新增在 sangfor 的菜单, 虽然说代码存在需要重构的地方
2017.05.21 修改 common_module 路径
2017.05.15 添加转盘页面选择地点功能
2017.03.22 添加有关备选菜单的相关代码实现
2017.03.10 将记录日记的装饰器装饰到对应视图上
"""
import logging

from django.http import Http404
from django.shortcuts import render

from common_module.common_help_function import log_wrapper
import my_constant as const

logger = logging.getLogger("my_blog.just_eating.views")

school_breakfast_backup_list = ["海棠-山东杂粮煎饼", "暂无其他早饭列表", "暂无其他早饭列表", "暂无其他早饭列表", "暂无其他早饭列表"]
school_lunch_backup_list = ["快餐", "微辣香锅", "新综香干炒肉", "食欲中西简餐", "暂无其他午饭列表", "暂无其他午饭列表"]
school_dinner_backup_list = ["海棠-瓦罐汤", "暂无其他晚饭列表", "暂无其他晚饭列表", "暂无其他晚饭列表", "暂无其他晚饭列表"]


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

    monday = const.EATING_MENU_STRUCTURE("周一", "海棠\n油饼夹菜", "新综\n台湾", "老综\n烤冷面")
    tuesday = const.EATING_MENU_STRUCTURE("周二", "丁香\n肉夹馍|鸡蛋饼卷", "丁香\n农家小炒肉", "新综\n沙县小吃")
    wednesday = const.EATING_MENU_STRUCTURE("周三", "竹园\n火腿饼", "竹园\n蒙古烤肉", "新综\n黑椒牛柳")
    thursday = const.EATING_MENU_STRUCTURE("周四", "老综\n卤肉卷", "新综\n包菜肉片", "新综\n快餐")
    friday = const.EATING_MENU_STRUCTURE("周五", "竹园\n手抓饼", "新综\n台湾", "丁香\n三楼自选快餐")
    saturday = const.EATING_MENU_STRUCTURE("周六", "海棠\n照烧鸡腿", "新综\n土豆丝炒肉", "老综\n锡纸烧")
    sunday = const.EATING_MENU_STRUCTURE("周日", "海棠\n鸡蛋灌饼|鸡蛋卷", "海棠\n川味椒盐里脊", "竹园\n快餐")

    for each_day in [monday, tuesday, wednesday, thursday, friday, saturday, sunday]:
        school_menu.append(each_day)

    return school_menu


def create_sangfor_menu():
    sangfor_menu = list()

    monday = const.EATING_MENU_STRUCTURE("周一", "公司\n炒米粉 + 牛奶", "公司\n6 楼", "公司\n金百合")
    tuesday = const.EATING_MENU_STRUCTURE("周二", "公司\n豆浆 + 油条", "公司\n8 楼", "公司\n4 | 2 楼")
    wednesday = const.EATING_MENU_STRUCTURE("周三", "公司\n牛奶 + 饼", "公司\n6 楼", "公司\n金百合")
    thursday = const.EATING_MENU_STRUCTURE("周四", "公司\n鸡蛋 + 粥", "公司\n6 楼麻辣烫", "公司\n8 楼")
    friday = const.EATING_MENU_STRUCTURE("周五", "公司\n豆浆 + 馒头|包子", "公司\n金百合", "公司\n4 | 2 楼")
    saturday = const.EATING_MENU_STRUCTURE("周六", "华里\n永和豆浆 + 奶黄包 + 其他包", "公司\n金百合 | 6 楼", "华里\n湘岳蒸菜馆")
    sunday = const.EATING_MENU_STRUCTURE("周日", "华里\n丰顺肠粉", "公司\n订外卖", "不知道去哪吃")

    for each_day in [monday, tuesday, wednesday, thursday, friday, saturday, sunday]:
        sangfor_menu.append(each_day)

    return sangfor_menu


@log_wrapper(str_format="查看了菜单", logger=logger)
def just_eating_home_view(request, eating_place):
    eating_times = ["", "早餐", "午餐", "晚餐"]

    if eating_place == "" or eating_place == "home":
        menu = create_home_menu()
        eating_place_name = "Home"
    elif eating_place == "school":
        menu = create_school_menu()
        eating_place_name = "School"
    elif eating_place == "sangfor":
        menu = create_sangfor_menu()
        eating_place_name = "Sangfor"
    else:
        raise Http404
    return render(request, "just_eating_base.html", {"eating_days": menu,
                                                     "eating_times": eating_times,
                                                     "eating_place": eating_place_name})


@log_wrapper(str_format="使用了随机选择食物的功能", logger=logger)
def random_eating(request, eating_place):
    if eating_place == "school_lunch":
        food_list = school_lunch_backup_list
        place = "学校午饭"
    elif eating_place == "school_dinner":
        food_list = school_dinner_backup_list
        place = "学校晚饭"
    else:
        raise Http404
    return render(request, "just_eating_spinner.html", {"food_list": food_list, "eating_place": place})
