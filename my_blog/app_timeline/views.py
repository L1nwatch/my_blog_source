# !/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 给 timeline app 设置 url 用的

2017.09.23 新增笔记
2017.07.13 新增 log 操作
2017.07.07 重构一下 event timeline 生成 html 的 方式
"""
# 标准库
from django.shortcuts import render
import logging

# 自己的模块
import my_constant as const
from common_module.common_help_function import log_wrapper

logger = logging.getLogger("my_blog.app_timeline.views")


def return_2018_events():
    """
    2018ing
    :return:
    """
    events = list()

    events.append(const.TRAVEL_EVENT_STRUCTURE("2", "May", "前海湾去西丽", ["对门下车"]))
    events.append(const.TRAVEL_EVENT_STRUCTURE("2", "May", "后海去前海湾", ["同门进出"]))
    events.append(const.TRAVEL_EVENT_STRUCTURE("2", "May", "前海湾去后海", ["同门进出"]))
    events.append(const.TRAVEL_EVENT_STRUCTURE("2", "May", "塘朗去前海湾", ["同门进出"]))
    events.append(const.TRAVEL_EVENT_STRUCTURE("1", "May", "深圳北去太安", ["同门进出"]))
    events.append(const.TRAVEL_EVENT_STRUCTURE("1", "May", "白石龙去深圳北", ["同门进出"]))
    events.append(const.TRAVEL_EVENT_STRUCTURE("1", "May", "龙胜去白石龙", ["同门进出"]))
    events.append(const.TRAVEL_EVENT_STRUCTURE("1", "May", "深圳北去龙胜", ["同门进出"]))
    events.append(const.TRAVEL_EVENT_STRUCTURE("1", "May", "桃源村去西丽", ["同门下车"]))
    events.append(const.TRAVEL_EVENT_STRUCTURE("1", "May", "太安去桃源村", ["同门下车"]))
    events.append(const.TRAVEL_EVENT_STRUCTURE("1", "May", "车公庙去西丽", ["对门下车"]))
    events.append(const.TRAVEL_EVENT_STRUCTURE("1", "May", "西丽去车公庙", ["同门下车"]))
    events.append(const.TRAVEL_EVENT_STRUCTURE("15", "April", "塘朗去留仙洞", ["同门进出"]))
    events.append(const.TRAVEL_EVENT_STRUCTURE("14", "April", "大学城去西丽", ["对门下车"]))
    events.append(const.TRAVEL_EVENT_STRUCTURE("14", "April", "西丽去大学城", ["同门进出"]))
    events.append(const.TRAVEL_EVENT_STRUCTURE("5", "April", "民治去西丽", ["对门进出"]))
    events.append(const.TRAVEL_EVENT_STRUCTURE("4", "April", "布吉去民治", ["同门下车"]))
    events.append(const.TRAVEL_EVENT_STRUCTURE("3", "April", "爱联到布吉", ["同门下车"]))
    events.append(const.TRAVEL_EVENT_STRUCTURE("2", "April", "布吉去爱联", ["同门下车"]))
    events.append(const.TRAVEL_EVENT_STRUCTURE("1", "April", "深圳北去布吉", ["对门下车"]))
    events.append(const.TRAVEL_EVENT_STRUCTURE("4", "Mar", "公司去灵芝", ["同门进出"]))
    events.append(const.TRAVEL_EVENT_STRUCTURE("4", "Feb", "灵芝去西丽", ["对门进出"]))
    events.append(const.TRAVEL_EVENT_STRUCTURE("4", "Jan", "西丽到桃源村", ["同门进出"]))

    return events


def return_2017_events():
    """
    2017 已经过去了
    :return:
    """
    events = list()
    events.append(const.TRAVEL_EVENT_STRUCTURE("12", "Nov", "公司去明治", ["同门进出"]))
    events.append(const.TRAVEL_EVENT_STRUCTURE("28", "Oct", "公司去灵芝", ["同门进出"]))
    events.append(const.TRAVEL_EVENT_STRUCTURE("3", "Oct", "西丽到民治天鸿公寓", ["10.17 上车,10.33 下车,对门进出"]))
    events.append(const.TRAVEL_EVENT_STRUCTURE("2", "Oct", "华茂苑到民治天鸿公寓", ["13.11 上车, 4 号线,清湖方向,到深圳北 13.19 点, 同门进出",
                                                                          "13.30 深圳北上车,去民治,对门进出,到民治 13.33 到",
                                                                          "民治 503 房间"]))
    events.append(const.TRAVEL_EVENT_STRUCTURE("2", "Oct", "西丽到华茂苑", ["11.10 从西丽地铁站出发,到深圳北 11.23 分, 同门进出",
                                                                      "11.31 上车 4 号线,福田方向,到上梅林下,a 口出,11.39 下车,同门进出"]))
    events.append(const.TRAVEL_EVENT_STRUCTURE("1", "Oct", "西丽到民治天鸿公寓", ["B 出口"]))
    events.append(const.TRAVEL_EVENT_STRUCTURE("24", "Sept", "西丽到世界之窗到公司",
                                               ["在西丽大概 14：15 左右出发，14：53 到世界之窗", "16.00 到宝安中心，坐地铁去公司，16.22 到塘朗，对门进出"]))
    events.append(const.TRAVEL_EVENT_STRUCTURE("24", "Sept", "深圳北+西丽+公司地铁", ["从深圳北去西丽是 同门下车", "从公司去深圳北是对门下车"]))
    events.append(const.TRAVEL_EVENT_STRUCTURE("24", "Sept", "汕头到深圳", [
        "8.16 在等 39 路，8.21 上公交，出发到客运中心站 8.30 点且买完票在等车了，8.58 上大巴，坐 9 点的大巴，没下雨，坐在右边，9.02 开车，右边不会晒太阳，左边晒到了，然后路上堵车了，去帝豪的路上堵了，9.24还堵在帝豪，到高铁站 10.23 ，直接进站过安检，10.33 上车",
        "D2327，10.45点发车，13.00点到深圳北站，13.02 上地铁，回到西丽 13.16 分,13.29吃牛肉汤河粉，12块是俩丸子+肉，还不错"]))
    events.append(const.TRAVEL_EVENT_STRUCTURE("22", "Sept", "公司到汕头",
                                               ["6.23 左右从公司出发，到深圳北18.46左右，等车等到19.06出发，坐19.21的高铁回潮汕，d2336",
                                                "到达潮汕站21.21分，北出口，21.49大巴发车，到达明珠广场 22.36分左右，走到家是22.55分，每隔15分钟有辆大巴，末班车是22.05"]))
    events.append(const.TRAVEL_EVENT_STRUCTURE("13", "July", "华里到公司",
                                               ["7.50 左右出门，出门左转的公交站，刚来就坐上 43 路，8.16 到南方科技大学，8.34 在六楼吃完早饭"]))
    events.append(const.TRAVEL_EVENT_STRUCTURE("08", "July", "华里出发去民治公寓", ["12分在塘朗站，16分在深圳北，18分到民治，25分到公寓"]))
    events.append(const.TRAVEL_EVENT_STRUCTURE("06", "July", "华里出发去 C3 栋", ["关于地铁的问题: 从酒店去公司，对门进出。从公司回来，同门进出，确定了。",
                                                                            "大概 8.15 到达公司，吃完饭约 8.30，到部门逛了逛大概 8.50 左右到 c3 栋阶梯教室（中间绕了远路）。"]))
    events.append(const.TRAVEL_EVENT_STRUCTURE("04", "July", "华里出发去金百合酒店",
                                               ["从华里酒店出发, 7.40 从房间下来，8.05 左右离开酒店，8.21 吃完早饭，8.27 坐上 36 路，8.30 到金百合酒店。"]))
    events.append(const.TRAVEL_EVENT_STRUCTURE("03", "July", "华里出发去金百合酒店",
                                               ["从华里酒店出发, 7.03 下楼, 大概 7.06 出发, 吃早餐 + 坐 36 路, 结果 7.43 到金百合。"]))
    events.append(const.TRAVEL_EVENT_STRUCTURE("02", "July", "华里出发去公司", [
        "从里寓服务公寓前往地铁站是 7 分钟, 坐地铁从大学城去塘朗站是 1.9 块, 好像是对门进出(但是从公司回大学城是同门进出), 地铁站下车走去公司是 8 分钟。"]))
    events.append(const.TRAVEL_EVENT_STRUCTURE("01", "July", "汕头出发去深圳", [
        "8.13 从家里坐小车前往客运站，8.23 到，注意火车站附近的大巴站是中心站，但是广东互联网售票没法买这里的票，所以下次还是自己过来买票吧。",
        "9 点上大巴，9.02 大巴开车，开车前半小时不能退票了，买票的时候注意一下。由于是下雨天，没太阳，所以坐哪边都一样。不过坐右边可以看自己的行李还在不在。",
        "10.05 到高铁站拿票，周末人很多，10.26 拿完票进站，二次安检完 10.34 坐下。等待 11.34 的高铁，到深圳北站是 13.48，高铁盒饭一盒 45（牛肉）。到大学城是 2.11 分。"]))
    events.append(const.TRAVEL_EVENT_STRUCTURE("28", "June", "西电回汕头", [
        "西稍门大酒店，4.30 醒来，5.30 出门，5.55 坐上大巴出发去机场，6.50 左右到机场，7.35 登机，8.15 飞机起飞，坐的是海南航空，没有平板可以玩，10.45 左右到深圳，11 点左右下飞机没上厕所直接去深圳北，12.20 到深圳北，检票进站花不到5分钟，坐的是 d7408，直接刷身份证即可，12.30 高铁出发，2.46 到潮汕站，2.50 买大巴票上车，东二线，3 点发车，坐了左边的位置，刚开始太阳一直晒，大概开了 10 分钟后，路线就不会晒到太阳了，到明珠广场下车，下车后加上骑自行车，回到家是 4 点"]))
    events.append(const.TRAVEL_EVENT_STRUCTURE("28", "June", "潮汕高铁大巴",
                                               ["票价 18 + 1 元保险", "东一线: 水果市场 -> 五矿物流城 -> 花园宾馆 -> 明珠广场 -> 天驰帝豪 -> 客运中心站",
                                                "东二线: 水果市场 -> 五矿物流城 -> 花园宾馆 -> 明珠广场 -> 维也纳酒店 -> 金海湾大酒店"]))
    return events


@log_wrapper(str_format="访问了时间线", level="info", logger=logger)
def travel_event_timeline(request):
    """
    负责记录 travel 时间的 timeline 视图函数
    :param request: Django 的 request 对象
    :return: 渲染过后的 html
    """
    events_2017 = return_2017_events()
    events_2018 = return_2018_events()

    return render(request, const.TRAVEL_EVENT_TIMELINE_TEMPLATE,
                  {"events_2017": events_2017, "events_2018": events_2018})
