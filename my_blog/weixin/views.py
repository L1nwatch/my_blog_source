# -*- coding: utf-8 -*-
# version: Python3.X
"""
2019-03-21 开始编写 微信公众号交互视图
"""

# 标准库
import logging
import hashlib
from django.shortcuts import render, redirect, HttpResponse

# 自己的模块
from common_module.common_help_function import log_wrapper

logger = logging.getLogger("my_blog.weixin.views")


def check_signature(signature, timestamp, nonce):
    L = [timestamp, nonce, "weixin_watch0_dot_top"]
    L.sort()
    s = L[0] + L[1] + L[2]
    return hashlib.sha1(s).hexdigest() == signature


@log_wrapper(str_format="服务器首次交互", level="info", logger=logger)
def check_signature_from_server(this_request):
    if this_request.method == "GET":
        with open("/opt/temp_weixin","w") as f:
            f.write(str(this_request.GET))
        return HttpResponse("OK")
    return HttpResponse("Need GET")
