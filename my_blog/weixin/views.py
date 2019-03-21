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
    hash_list = ["490772448", timestamp, nonce]
    hash_list.sort()
    hash_str = "".join([x for x in hash_list])
    hash_result = hashlib.sha1(hash_str).hexdigest()
    if hash_result == signature:
        return True
    else:
        return False


@log_wrapper(str_format="服务器首次交互", level="info", logger=logger)
def check_signature_from_server(this_request):
    print("[*] 有人访问")
    if this_request.method == "GET":
        signature = this_request.GET.get("signature")
        echostr = this_request.GET.get("echostr")
        timestamp = this_request.GET.get("timestamp")
        nonce = this_request.GET.get("nonce")
        if check_signature(signature, timestamp, nonce):
            # logger.info("[!] 微信服务器校验成功")
            print("[!] 微信服务器校验成功")
            return echostr
        else:
            # logger.error("[-] 微信服务器校验失败")
            print("[-] 微信服务器校验失败")
            raise Http404
    raise Http404
