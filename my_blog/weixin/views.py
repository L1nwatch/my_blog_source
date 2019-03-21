# -*- coding: utf-8 -*-
# version: Python3.X
"""
2019-03-21 开始编写 微信公众号交互视图
"""

# 标准库
import logging
import hashlib
from django.shortcuts import render, redirect, Http404, HttpResponse
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException

# 自己的模块
from common_module.common_help_function import log_wrapper

logger = logging.getLogger("my_blog.weixin.views")


@log_wrapper(str_format="服务器首次交互", level="info", logger=logger)
def check_signature_from_server(this_request):
    if this_request.method == "GET":
        signature = this_request.GET.get("signature", None)
        echostr = this_request.GET.get("echostr", None)
        timestamp = this_request.GET.get("timestamp", None)
        nonce = this_request.GET.get("nonce", None)
        try:
            check_signature("lf490772448", signature, timestamp, nonce)
            return HttpResponse(echostr)
        except InvalidSignatureException as e:
            raise Http404
