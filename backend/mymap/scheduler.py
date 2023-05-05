from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
from django.db.models import F
from django.utils import timezone

from .models import ScheduledAccountDeletion


def delete_users_due():
    due_account_deletions = ScheduledAccountDeletion.objects.filter(request_date__lte=timezone.now() - F('interval'))
    accounts_count = len(due_account_deletions)
    if accounts_count > 0:
        for due_account_deletion in due_account_deletions:
            user = due_account_deletion.user
            print("Account deleted: " + user.email + " (" + user.username + ")")
            user.delete()
        print(str(accounts_count) + " accounts deleted in total.")
    print("No accounts were due to be deleted.")



def start_scheduler():
    def _scheduler_listener(event):
        if event.exception:
            print("The scheduler crashed.")

    scheduler = BackgroundScheduler()

    # Every 4 hours
    scheduler.add_job(delete_users_due, trigger='interval', hours=4)

    # To test quickly (10s delay between checks), uncomment line below.
    # scheduler.add_job(delete_users_due, trigger='interval', seconds=10)

    scheduler.add_listener(_scheduler_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

    scheduler.start()