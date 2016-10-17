from django_cron import CronJobBase, Schedule

from articles.views import update_notes


class AutoUpdateNotes(CronJobBase):
    RUN_EVERY_MINS = 120  # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'django_cron.AutoUpdateNotes'  # a unique code

    def do(self):
        update_notes()
