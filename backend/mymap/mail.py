from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mass_mail
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.conf import settings

from .models import Message

User = get_user_model()


def _get_unread_messages_count(user):
    return Message.objects.filter(
        Q(conversation__owner=user) | Q(conversation__buyer=user),
        Q(seen=False), ~Q(user=user)
    ).count()


def _get_new_items_near_user(user):
    #get items within distance
    #among close items, get ones which startdate are less than 24h ?
    return []


def _prepare_mail_user(user):
    unread_count = _get_unread_messages_count(user)
    new_items = _get_new_items_near_user(user)

    # TODO: use template for emails
    # https://django-mail-templated.readthedocs.io/en/master/ ?

    if unread_count > 0 and len(new_items) == 0:
        subject = "You have {} unread messages on Shareish".format(unread_count)
        message = "Dear {} {} ({}),{}You have {} unread messages on Shareish ({}).{}Please log in using your e-mail address to read them in the Conversations tab. ".format(
            user.first_name, user.last_name, user.username, "\n\n", unread_count, settings.APP_URL, "\n\n")
        #print(message)

    elif unread_count > 0 and len(new_items) > 0:
        subject = "You have {} unread messages on Shareish and {} new items near you".format(
            unread_count, len(new_items)
        )
        message = "Dear {} {} ({}), you have {} unread messages on Shareish ({}) and {} new items near you.".format(
            user.first_name, user.last_name, user.username, unread_count, settings.APP_URL, len(new_items)
        )
    elif len(new_items) > 0:
        subject = "There are {} new items near you on Shareish".format(len(new_items))
        message = "Dear {} {} ({}), there are {} new items near you on Shareish ({}).".format(
            user.first_name, user.last_name, user.username, len(new_items), settings.APP_URL
        )
    else:
        # Nothing new, abort
        return None

    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]

    return subject, message, from_email, recipient_list


# To be scheduled
def send_emails():
    # Get all activated users
    users = User.objects.filter(is_active=True)

    # For each user, prepare mail to send (if any)
    to_send = []
    for user in users:
        mail = _prepare_mail_user(user)
        if mail:
            to_send.append(mail)

    # Send list of prepared mails
    # https://docs.djangoproject.com/en/4.1/topics/email/#send-mass-mail
    # https://docs.djangoproject.com/en/4.1/topics/email/#send-mail
    # It uses EMAIL_* parameters from settings.py
    if len(to_send) > 0:
        delivered = send_mass_mail(
            to_send,
            fail_silently=True,
        )
        print("Successfully delivered {}/{} emails".format(delivered, len(to_send)))
    else:
        print("No scheduled emails to send.")


def start_mail_scheduler():
    def _scheduler_listener(event):
        if event.exception:
            print('The scheduled email sending crashed.')
        else:
            print('The scheduled email sending worked.')

    scheduler = BackgroundScheduler()
    scheduler.add_job(send_emails, trigger='cron', hour=8, minute=0)
    # TO TEST quickly, uncomment this line:
    #scheduler.add_job(send_emails, trigger='cron', second=0)
    # To configure cron:
    # https://apscheduler.readthedocs.io/en/latest/modules/triggers/cron.html?highlight=cron
    scheduler.add_listener(_scheduler_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    scheduler.start()


