# backend/mymap/cron.py

from django.core import management
from django_cron import CronJobBase, Schedule

class BackupAndMedia(CronJobBase):
    RUN_AT_TIMES = ['03:00']
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    
    code = 'mymap.BackupAndMedia'

    def do(self):
        management.call_command('dbbackup', compress=False, clean=True, interactive=False)
        management.call_command('mediabackup', compress=True, clean=True, interactive=False)