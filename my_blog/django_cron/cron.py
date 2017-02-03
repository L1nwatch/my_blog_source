from django_cron import CronJobBase, Schedule
import threading

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
        notes_update_thread = threading.Thread(target=update_notes, args=())
        journals_update_thread = threading.Thread(target=update_journals, args=())

        notes_update_thread.start()
        journals_update_thread.start()

        print("[*] [{}] {separator} 进行定时更新 {separator}".format(now, separator="*" * 30))
