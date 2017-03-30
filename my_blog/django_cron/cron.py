#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.03.30 新增 code_collect 更新操作
2017.03.05 改多线程更新变为多进程更新
"""

from django_cron import CronJobBase, Schedule
import multiprocessing

from articles.views import update_notes
from work_journal.views import update_journals
from gitbook_notes.views import update_gitbook_codes
from code_collect.views import code_collect

import datetime


class AutoUpdateNotes(CronJobBase):
    RUN_EVERY_MINS = 120  # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'django_cron.AutoUpdateNotes'  # a unique code

    @staticmethod
    def do():
        now = datetime.datetime.today()
        jobs = list()

        # 多进程更新
        for func in [update_notes, update_journals, update_gitbook_codes, code_collect]:
            p = multiprocessing.Process(target=func, args=())
            jobs.append(p)
            p.start()

        for process in jobs:
            process.join()

        print("[*] [{}] {separator} 进行定时更新 {separator}".format(now, separator="*" * 30))
