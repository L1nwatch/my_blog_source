# !/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 给 timeline app 设置 url 用的

2017.07.07 重构一下 event timeline 生成 html 的 方式
"""
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
    events = list()
    events.append(const.TRAVEL_EVENT_STRUCTURE("06", "July", "华里出发去 C3 栋", ["关于地铁的问题: 从酒店去公司，对门进出。从公司回来，同门进出，确定了。","大概 8.15 到达公司，吃完饭约 8.30，到部门逛了逛大概 8.50 左右到 c3 栋阶梯教室（中间绕了远路）。"]))
    events.append(const.TRAVEL_EVENT_STRUCTURE("04", "July", "华里出发去金百合酒店", ["从华里酒店出发, 7.40 从房间下来，8.05 左右离开酒店，8.21 吃完早饭，8.27 坐上 36 路，8.30 到金百合酒店。"]))
    events.append(const.TRAVEL_EVENT_STRUCTURE("03", "July", "华里出发去金百合酒店", ["从华里酒店出发, 7.03 下楼, 大概 7.06 出发, 吃早餐 + 坐 36 路, 结果 7.43 到金百合。"]))
    events.append(const.TRAVEL_EVENT_STRUCTURE("02", "July", "华里出发去公司", ["从里寓服务公寓前往地铁站是 7 分钟, 坐地铁从大学城去塘朗站是 1.9 块, 好像是对门进出(但是从公司回大学城是同门进出), 地铁站下车走去公司是 8 分钟。"]))
    events.append(const.TRAVEL_EVENT_STRUCTURE("01", "July", "汕头出发去深圳", ["8.13 从家里坐小车前往客运站，8.23 到，注意火车站附近的大巴站是中心站，但是广东互联网售票没法买这里的票，所以下次还是自己过来买票吧。", "9 点上大巴，9.02 大巴开车，开车前半小时不能退票了，买票的时候注意一下。由于是下雨天，没太阳，所以坐哪边都一样。不过坐右边可以看自己的行李还在不在。", "10.05 到高铁站拿票，周末人很多，10.26 拿完票进站，二次安检完 10.34 坐下。等待 11.34 的高铁，到深圳北站是 13.48，高铁盒饭一盒 45（牛肉）。到大学城是 2.11 分。"]))
    events.append(const.TRAVEL_EVENT_STRUCTURE("28", "June", "西电回汕头", ["西稍门大酒店，4.30 醒来，5.30 出门，5.55 坐上大巴出发去机场，6.50 左右到机场，7.35 登机，8.15 飞机起飞，坐的是海南航空，没有平板可以玩，10.45 左右到深圳，11 点左右下飞机没上厕所直接去深圳北，12.20 到深圳北，检票进站花不到5分钟，坐的是 d7408，直接刷身份证即可，12.30 高铁出发，2.46 到潮汕站，2.50 买大巴票上车，东二线，3 点发车，坐了左边的位置，刚开始太阳一直晒，大概开了 10 分钟后，路线就不会晒到太阳了，到明珠广场下车，下车后加上骑自行车，回到家是 4 点"]))
    events.append(const.TRAVEL_EVENT_STRUCTURE("28", "June", "潮汕高铁大巴", ["票价 18 + 1 元保险","东一线: 水果市场 -> 五矿物流城 -> 花园宾馆 -> 明珠广场 -> 天驰帝豪 -> 客运中心站","东二线: 水果市场 -> 五矿物流城 -> 花园宾馆 -> 明珠广场 -> 维也纳酒店 -> 金海湾大酒店"]))

    return render(request, const.TRAVEL_EVENT_TIMELINE_TEMPLATE, {"events": events})
