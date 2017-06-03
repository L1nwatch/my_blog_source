#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 负责发送邮件

2017.06.03 继续重写代码逻辑, 避免数据库锁定以及发邮件卡顿的问题
2017.06.02 更改检索数据库 IP 的代码, 避免由于多线程导致没法立即检索数据库然后抛出异常
2017.05.30 完善发送邮件的内容, 邮件标题加上访问 IP 的地理信息
2017.05.26 修正代码逻辑, 要不然子线程中无法捕获异常也不会记录发送邮件失败的日志
2017.05.25 改为多线程, 避免邮件发送失败时导致前端也显示不了了
2017.05.25 新建一个发送邮件类, 专门负责发送邮件
"""
# 自己的模块
from common_module.models import VisitedIP
from common_module.ip_deal import locate_using_ip_address
from my_constant import const

# 标准库
from django.core.mail import send_mail
from django.db.utils import OperationalError
import threading
import time

__author__ = '__L1n__w@tch'


class EmailSend:
    def __init__(self, want_send_email=True):
        self.send_email_flag = want_send_email  # flag, 用来表示用户是否想要进行发送邮件的操作
        self.send_email_success = True  # True 表示到目前为止邮件发送系统没有故障, 可以继续发送

    @staticmethod
    def is_new_ip_address(ip_address):
        """
        判断是否是新的 IP 地址, 同时更新计数器
        :return: True or False, 新 IP 地址则为 True
        """
        while True:
            try:
                ip, created = VisitedIP.objects.get_or_create(ip_address=ip_address)
                ip.times += 1
                ip.save()
                return created
            except OperationalError:
                time.sleep(1)

        return False

    def want_to_send_email(self, ip_address):
        """
        判断是否要进行发送邮件操作
        :param ip_address: str(), 表示访问者的 IP 地址
        :return: True or False, True 表示希望发送邮件
        """
        # IP 查询, IP 第一次出现则发送邮件
        # 检查之前几次邮件是否发送成功, 失败则不再发送
        # 检查相关信息是否完整, 完整才进行发送
        if self.send_email_flag and self.send_email_success and self.is_new_ip_address(ip_address):
            return True
        else:
            return False

    def try_to_send_email(self, message, logger, ip_address, location):
        """
        尝试发送邮件, 并进行异常捕获
        :param message: str(), 邮件正文
        :param logger: logger 对象, 日志记录使用
        :param ip_address: str(), ip 地址
        :param location: str(), 表示 IP 地址的地理位置
        :return:
        """
        logger.info("[*] 开始尝试发送邮件")

        try:
            send_mail(subject="[!] {} 的某人访问了你的网站".format(location), message=message, from_email="watch@watch0.top",
                      recipient_list=["490772448@qq.com"], fail_silently=False)
            logger.info("[*] 邮件发送成功")
        except Exception as e:
            self.send_email_success = False
            logger.error("[*] 发送失败: {}".format(e))

    def send_email(self, *, message, ip_address, logger, send_email_check, location):
        """
        发送邮件
        :param message: str(), 邮件正文
        :param ip_address: str(), 表示访问者的 IP 地址
        :param logger: logger 对象, 日志记录使用
        :param send_email_check: boolean(), True or False, 表示 Email 发送检查是否通过
        :param location: str(), 表示 IP 地址的地理位置
        :return: str(), 如果执行异常则返回消息方便记录到日志中, 没异常则返回空字符串
        """
        if send_email_check:
            self.try_to_send_email(message, logger, ip_address, location)


email_sender = EmailSend(want_send_email=const.WANT_SEND_EMAIL)

if __name__ == "__main__":
    pass
