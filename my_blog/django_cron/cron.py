from django_cron import CronJobBase, Schedule

from articles.views import update_notes
from work_journal.views import update_journals

import datetime


class AutoUpdateNotes(CronJobBase):
    RUN_EVERY_MINS = 120  # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'django_cron.AutoUpdateNotes'  # a unique code

    @staticmethod
    def do():
        now = datetime.datetime.today()
        update_notes()
        print("[*] [{}] {separator} 定时更新结束 {separator}".format(now, separator="*" * 30))
