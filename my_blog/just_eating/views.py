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

    monday = const.EATING_MENU_STRUCTURE("周一", "香麦馒头+奶黄包+五谷杂粮", "白菜炒腐竹", "白菜炒香菇")  # 纯素
    tuesday = const.EATING_MENU_STRUCTURE("周二", "流沙包+白馒头+五谷杂粮", "火锅-牛肉丸粿条",
                                          ("黑椒牛柳\n"
                                           "肥牛\n"
                                           "青椒炒牛肉\n")
                                          )  # 牛肉
    wednesday = const.EATING_MENU_STRUCTURE("周三", "手抓饼+豆浆", "青椒鸡蛋", "蚝油生菜")  # 纯素
    thursday = const.EATING_MENU_STRUCTURE("周四", "卤肉卷",
                                           ("包菜肉\n"
                                            "腐竹肉\n"
                                            "香干肉\n"
                                            "香菇肉片\n"
                                            "杏鲍菇炒肉\n"),
                                           ("糖醋里脊\n"
                                            "椒盐里脊\n"
                                            "酸汤丸子+酥肉\n")
                                           )  # 猪肉
    friday = const.EATING_MENU_STRUCTURE("周五", "鸡蛋灌饼/鸡蛋卷饼/照烧鸡腿", "千叶豆腐", "家常炒河粉")  # 纯素
    saturday = const.EATING_MENU_STRUCTURE("周六", "肉夹馍",
                                           ("鸡块\n"
                                            "炸鸡腿\n"
                                            "宫保鸡丁\n"
                                            "猪肚鸡\n"),
                                           ("香菇滑鸡\n"
                                            "脆皮鸡\n"
                                            "黄焖鸡\n")
                                           )  # 鸡肉
    sunday = const.EATING_MENU_STRUCTURE("周日", "肠粉", "当归牛腩",
                                         ("奥尔良烤肉\n"
                                          "虾条\n")
                                         )  # 新奇

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

    monday = const.EATING_MENU_STRUCTURE("周一", "公司\n4 楼炒米粉", "公司\n2 楼酸汤牛肉鱼", "公司\n快餐")
    tuesday = const.EATING_MENU_STRUCTURE("周二", "公司\n4 楼面包", "公司\n4 楼冒菜", "公司\n快餐")
    wednesday = const.EATING_MENU_STRUCTURE("周三", "公司\n2 楼粿条", "公司\n金百味", "公司\n2 楼包子")
    thursday = const.EATING_MENU_STRUCTURE("周四", "公司\n4 楼肠粉", "公司\n4 楼牛肉饭", "公司\n快餐")
    friday = const.EATING_MENU_STRUCTURE("周五", "公司\n2 楼面包", "公司\n快餐", "公司\n8 楼")
    saturday = const.EATING_MENU_STRUCTURE("周六", "西丽\n红糖馒头+奶黄包+豆浆", "公司\n金百合", "不知道去哪吃")
    sunday = const.EATING_MENU_STRUCTURE("周日", "西丽\n双蛋肠粉", "公司\n订外卖", "不知道去哪吃")

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
