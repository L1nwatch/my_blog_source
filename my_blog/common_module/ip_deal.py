#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 专门存放 IP 相关的处理函数

2017.05.30 产生了交叉引用, 于是把 IP 相关的都提取出来放在这个脚本之中
"""
# 标准库
import ipaddress
from ipware.ip import get_ip, get_real_ip, get_trusted_ip
import requests

try:
    import simplejson as json
except ImportError:
    import json

__author__ = '__L1n__w@tch'


def locate_using_ip_address(ip_address):
    """
    根据 IP 地址定位地理位置, 中国则返回具体市县, 其他国家则只返回国家
    :param ip_address: str(), 比如 "113.140.11.123"
    :return: str(), 比如 "中国-西安市"
    """
    if ipaddress.ip_address(ip_address).is_private:
        return "内网 IP"

    response = requests.get("http://ip.taobao.com/service/getIpInfo.php?ip={ip_address}".format(ip_address=ip_address))
    result = json.loads(response.content.decode("unicode_escape"))
    country = result["data"]["country"]

    if country == "中国":
        return "{}-{}".format(country, result["data"]["city"])
    else:
        return country


def get_ip_from_django_request(request):
    """
    # 用来获取访问者 IP 的
    # 参考
    ## https://my.oschina.net/u/167994/blog/156184
    ## http://stackoverflow.com/questions/4581789/how-do-i-get-user-ip-address-in-django
    :param request: 传给视图函数的 request
    :return: ip 地址, 比如 116.26.110.36
    """
    return get_ip(request)


