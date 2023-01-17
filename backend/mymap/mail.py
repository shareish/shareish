from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mass_mail
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta, time
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point

from .models import Message
from .models import Item

User = get_user_model()


def _get_unread_messages_count(user):
    return Message.objects.filter(
        Q(conversation__owner=user) | Q(conversation__buyer=user),
        Q(seen=False), ~Q(user=user)
    ).count()


def _get_new_items_near_user(user):
    #get items within user dwithin distance and which stardate is between yesterday and today, not event
    #print("-------------- in _get_new_items_near_user for " +user.username + "----------------")
    today = datetime.now().date()
    yesterday = today - timedelta(1)
    if user.ref_location:
        pnt = user.ref_location
    else:
        pnt = Point(0.0, 0.0)
    return Item.objects.filter(
        Q(creationdate__lte = today, creationdate__gte = yesterday),
        Q(location__dwithin=(pnt,D(km=user.dwithin_notifications))),
        ~Q(item_type='EV'),
        ~Q(user=user))   #~Q for items from another user


def _get_events_near_user(user):
    #get items (events) within user dwithin distance 
    today = datetime.now().date()
    yesterday = today - timedelta(1)
    if user.ref_location:
        pnt = user.ref_location
    else:
        pnt = Point(0.0, 0.0)
    return Item.objects.filter(
        Q(item_type='EV'),
        Q(creationdate__lte = today, creationdate__gte = yesterday),
        Q(location__dwithin=(pnt,D(km=user.dwithin_notifications))),
        ~Q(user=user))   #~Q for items from another user

def _prepare_mail_user(user):
    new_items = _get_new_items_near_user(user)
    unread_count = _get_unread_messages_count(user)
    new_events = _get_events_near_user(user)

    # TODO: use template for emails
    # https://django-mail-templated.readthedocs.io/en/master/ ?
    
    if unread_count > 0:
        subject_msg="{} unread message".format(unread_count)
        if unread_count > 1:
            subject_msg+="s"
    else:
        subject_msg=""
        
    if len(new_items) > 0:
        subject_items="{} new item".format(len(new_items))
        if len(new_items) > 1:
            subject_items+="s"
    else:
        subject_items=""
        
    if len(new_events) > 0:
        subject_events="{} new event".format(len(new_events))
        if len(new_events) > 1:
            subject_events+="s"
    else:
        subject_events=""
    
    if unread_count > 0 or len(new_items) > 0 or len(new_events) > 0:
        subject = "[Shareish] Recent content on Shareish mutual aid platform ({} {} {})".format(subject_msg,subject_items,subject_events)
        message = "Dear {} {} ({}),\n\nThere is new content since yesterday within your neighbourhood on Shareish mutual aid platform.\n".format(
            user.first_name, user.last_name, user.username)
        message+="Please login on {} (using your e-mail address) to view it.\n\n".format(settings.APP_URL)
    
        if unread_count > 0:
            if unread_count > 1:
                plural="s"
            else:
                plural=""
            message += "You have {} unread message{}, available in the Conversations tab.\n\n".format(unread_count,plural)
        if len(new_items) > 0:
            if len(new_items)>1:
                plural="s"
            else:
                plural=""
            message += "You have {} new item{}, available in the Map or Browse tab:\n".format(len(new_items),plural)
            for i in range (len(new_items)):
                message+="* {} ({}, within {} km)\n".format(new_items[i].name, new_items[i].get_item_type_display(), round(100*new_items[i].location.distance(user.ref_location),2))
        if len(new_events) > 0:
            if len(new_events)>1:
                plural="s"
            else:
                plural=""
            message += "\nYou have {} new event{}, available in the Map or Browse tab:\n".format(len(new_events),plural)
            for i in range (len(new_events)):
                message+="* {} (from {} to {}, within {} km)\n".format(new_events[i].name, new_events[i].startdate, new_events[i].enddate, round(100*new_events[i].location.distance(user.ref_location),2))

        message+="\nThese notifications can be configured on Shareish in My account - Edit."
        message+="\n\nThe Shareish team.\n"

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


