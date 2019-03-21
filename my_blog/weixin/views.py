# -*- coding: utf-8 -*-
# version: Python3.X
"""
2019-03-21 开始编写 微信公众号交互视图
"""

# 标准库
import logging
import hashlib
from django.shortcuts import render, redirect, Http404

# 自己的模块
from common_module.common_help_function import log_wrapper

logger = logging.getLogger("my_blog.weixin.views")


def check_signature(signature, timestamp, nonce):
    # L = [timestamp, nonce, 490772448]
    # L.sort()
    # s = L[0] + L[1] + L[2]
    # hash_code = hashlib.sha1(s).hexdigest()
    # return hash_code == signature
    hash_list = ["wx1", timestamp, nonce]
    hash_list.sort()
    sha1 = hashlib.sha1()
    map(sha1.update,hash_list)
    hash_result = sha1.hexdigest()
    if hash_result == signature:
        return True
    else:
        return False


@log_wrapper(str_format="服务器首次交互", level="info", logger=logger)
def check_signature_from_server(this_request):
    if this_request.method == "GET":
        signature = this_request.GET.get("signature")
        echostr = this_request.GET.get("echostr")
        timestamp = this_request.GET.get("timestamp")
        nonce = this_request.GET.get("nonce")
        # check_signature(signature, timestamp, nonce)
        return echostr
    raise Http404
