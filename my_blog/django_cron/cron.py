#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.06.03 剔除更新笔记数的功能, 因为某些不知名的原因导致出 BUG 了
2017.06.02 新增更新笔记数的功能
2017.05.20 添加日志打包功能
2017.03.30 新增 code_collect 更新操作
2017.03.05 改多线程更新变为多进程更新
"""

# 标准库
from django_cron import CronJobBase, Schedule
from django.conf import settings

import multiprocessing
import datetime
import os

# 自己的模块
from articles.views import update_notes
from work_journal.views import update_journals
from gitbook_notes.views import update_gitbook_codes
from code_collect.views import code_collect
from log_file_deal.log_packer import LogPacker


class AutoUpdateNotes(CronJobBase):
    RUN_EVERY_MINS = 1  # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'django_cron.AutoUpdateNotes'  # a unique code

    @staticmethod
    def do():
        log_path = os.path.join(os.path.dirname(os.path.dirname(settings.BASE_DIR)), "log")
        log_deal = LogPacker(log_path)
        now = datetime.datetime.today()
        jobs = list()

        # 多进程更新
        # 包括更新文章、更新日志、更新 GitBook、更新代码数据库、日志压缩
        for func in [update_notes, update_journals, update_gitbook_codes, code_collect, log_deal.run]:
            p = multiprocessing.Process(target=func, args=())
            jobs.append(p)
            p.start()

        for process in jobs:
            process.join()

        print("[*] [{}] {separator} 进行定时更新 {separator}".format(now, separator="*" * 30))

