from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
from django.db import transaction
from django.db.models import F
from django.utils import timezone

from .models import ScheduledAccountDeletion, ConversationUser


def delete_users_due():
    due_account_deletions = ScheduledAccountDeletion.objects.filter(request_date__lte=timezone.now() - F('interval'))
    accounts_count = len(due_account_deletions)
    if accounts_count > 0:
        for due_account_deletion in due_account_deletions:
            try:
                with transaction.atomic():
                    user = due_account_deletion.user

                    # Delete all the conversations where the user to delete was the last one inside
                    conversations_user_to_check = ConversationUser.objects.filter(user=user)
                    for conversation_user_to_check in conversations_user_to_check:
                        conversation = conversation_user_to_check.conversation
                        if conversation.users.count() == 1:
                            conversation_id = conversation.id
                            conversation.delete()
                            print("Conversation #{} deleted (nobody left inside)".format(conversation_id))

                    id, email, username = user.id, user.email, user.username

                    # Delete the account
                    user.delete()

                    print("Account #{} deleted: {} ({})".format(id, email, username))
            except Exception as e:
                print("INTERNAL ERROR: Couldn't delete user {} ({}) ({})".format(
                    due_account_deletion.user.email,
                    due_account_deletion.user.username,
                    str(e)
                ))
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