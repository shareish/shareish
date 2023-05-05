from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
from apscheduler.schedulers.background import BackgroundScheduler
from django.core import mail
from django.contrib.auth import get_user_model
from django.db.models import Q, F
from django.conf import settings
from datetime import datetime, timedelta
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from django.urls import reverse

from mail_templated import EmailMessage

from .models import Message, MailNotificationFrequencies
from .models import Item

User = get_user_model()

# Time required between two conversation messages to be
# considered new and sending an email notification (in minutes)
delay_instant_notif_conversations = 10

to_show = {
    'conversations': 3,
    'items': 5,
    'events': 3
}

item_types = {
    "DN": "Donation",
    "LN": "Loan",
    "RQ": "Request",
    "EV": "Event"
}


def _get_unread_messages(user):
    messages = Message.objects.filter(
        Q(conversation__owner=user) | Q(conversation__buyer=user),
        Q(seen=False), ~Q(user=user)
    )

    return messages[:to_show['conversations']], messages.count()


def _get_last_new_items_near_user(user, frequency: MailNotificationFrequencies):
    end = datetime.now().date()
    if frequency == MailNotificationFrequencies.DAILY:
        start = end - timedelta(days=1)
    elif frequency == MailNotificationFrequencies.WEEKLY:
        start = end - timedelta(days=7)
    else:
        return [], 0

    # Items sorted by distance
    queryset = Item.objects.filter(
        Q(creationdate__gte=start),
        Q(location__dwithin=(user.ref_location, D(km=user.dwithin_notifications))),
        ~Q(type='EV'),
        ~Q(user=user)
    ).annotate(distance=Distance("location", user.ref_location)).order_by("distance")

    return queryset[:to_show['items']], queryset.count()


def _get_last_new_events_near_user(user, frequency: MailNotificationFrequencies):
    end = datetime.now().date()
    if frequency == MailNotificationFrequencies.DAILY:
        start = end - timedelta(days=1)
    elif frequency == MailNotificationFrequencies.WEEKLY:
        start = end - timedelta(days=7)
    else:
        return [], 0

    # Events sorted by delay before event starting
    queryset = Item.objects.filter(
        Q(type='EV'),
        Q(creationdate__gte=start),
        Q(location__dwithin=(user.ref_location, D(km=user.dwithin_notifications))),
        ~Q(user=user)
    ).annotate(
        delay=F('startdate') - end,
        distance=Distance("location", user.ref_location)
    ).order_by("delay")

    return queryset[:to_show['events']], queryset.count()


def send_mail_notif_new_message_received(conversation, message_content, sender, receiver):
    connection = mail.get_connection(fail_silently=True)

    context = {
        "receiver": receiver,
        "sender": sender,
        "conversation": conversation,
        "message_content": message_content,
        "app_url": settings.APP_URL
    }

    email = EmailMessage(
        'emails/notif_new_message_received.tpl',
        context,
        settings.EMAIL_HOST_USER,
        [receiver.email],
        connection=connection
    )

    if not email.is_rendered:
        email.render()

    email.send()

    print("Successfully delivered instant conversation email notification")


def send_mail_notif_new_single_event_published(event, user_that_published):
    users = User.objects.filter(
        Q(is_active=True),
        Q(mail_notif_freq_events=MailNotificationFrequencies.INSTANTLY),
        Q(ref_location__isnull=False),
        ~Q(pk=user_that_published.id)
    ).annotate(
        distance_from_event=Distance("ref_location", event.location)
    ).filter(distance_from_event__lte=F("dwithin_notifications") * 1000)

    connection = mail.get_connection(fail_silently=True)
    to_send = []

    for user in users:
        context = {
            "user": user,
            "event": event,
            "app_url": settings.APP_URL
        }

        email = EmailMessage('emails/notif_new_single_event_published.tpl', context, settings.EMAIL_HOST_USER,
                             [user.email], connection=connection)

        if not email.is_rendered:
            email.render()

        to_send.append(email)

    if len(to_send) > 0:
        delivered = connection.send_messages(to_send)
        print("Successfully delivered {}/{} emails".format(delivered, len(to_send)))


def send_mail_notif_new_single_item_published(item, user_that_published):
    users = User.objects.filter(
        Q(is_active=True),
        Q(mail_notif_freq_items=MailNotificationFrequencies.INSTANTLY),
        Q(ref_location__isnull=False),
        ~Q(pk=user_that_published.id)
    ).annotate(
        distance_from_item=Distance("ref_location", item.location)
    ).filter(distance_from_item__lte=F("dwithin_notifications") * 1000)

    connection = mail.get_connection(fail_silently=True)
    to_send = []

    for user in users:
        context = {
            "user": user,
            "item": item,
            "type": item_types[item.type],
            "app_url": settings.APP_URL
        }

        email = EmailMessage('emails/notif_new_single_item_published.tpl', context, settings.EMAIL_HOST_USER,
                             [user.email], connection=connection)

        if not email.is_rendered:
            email.render()

        to_send.append(email)

    if len(to_send) > 0:
        delivered = connection.send_messages(to_send)
        print("Successfully delivered {}/{} emails".format(delivered, len(to_send)))


def _prepare_mail_notif_conversations(user, frequency: MailNotificationFrequencies, connection):
    # Get the messages don't take into account the frequency
    # It takes all the pending conversations
    unread_messages, n = _get_unread_messages(user)

    if n > 0:
        if frequency == MailNotificationFrequencies.DAILY:
            digest = "Daily conversations digest"
        else:
            digest = "Recent conversations"

        context = {
            "digest": digest,
            "n": n,
            "user": user,
            "unread_messages": unread_messages,
            "app_url": settings.APP_URL,
            "to_show": to_show['conversations']
        }

        email = EmailMessage(
            'emails/notif_digest_conversations.tpl',
            context,
            settings.EMAIL_HOST_USER,
            [user.email],
            connection=connection
        )

        if not email.is_rendered:
            email.render()

        return email


def _prepare_mail_notif_events(user, frequency: MailNotificationFrequencies, connection):
    new_events, n = _get_last_new_events_near_user(user, frequency)

    if n > 0:
        if frequency == MailNotificationFrequencies.DAILY:
            digest = "Daily events digest"
        elif frequency == MailNotificationFrequencies.WEEKLY:
            digest = "Weekly events digest"
        else:
            digest = "Recent events"

        context = {
            "digest": digest,
            "n": n,
            "user": user,
            "new_events": new_events,
            "app_url": settings.APP_URL,
            "to_show": to_show['events']
        }

        email = EmailMessage(
            'emails/notif_digest_events.tpl',
            context,
            settings.EMAIL_HOST_USER,
            [user.email],
            connection=connection
        )

        if not email.is_rendered:
            email.render()

        return email


def _prepare_mail_notif_items(user, frequency: MailNotificationFrequencies, connection):
    new_items, n = _get_last_new_items_near_user(user, frequency)

    if n > 0:
        if frequency == MailNotificationFrequencies.DAILY:
            digest = "Daily items digest"
        elif frequency == MailNotificationFrequencies.WEEKLY:
            digest = "Weekly items digest"
        else:
            digest = "Recent items"

        context = {
            "digest": digest,
            "n": n,
            "user": user,
            "new_items": new_items,
            "app_url": settings.APP_URL,
            "item_types": item_types,
            "to_show": to_show['items']
        }

        email = EmailMessage(
            'emails/notif_digest_items.tpl',
            context,
            settings.EMAIL_HOST_USER,
            [user.email],
            connection=connection
        )

        if not email.is_rendered:
            email.render()

        return email


def send_mail_recover_account(user, token):
    connection = mail.get_connection(fail_silently=True)
    to_send = []

    context = {
        "user": user,
        "recover_account_token_url": settings.APP_URL + "/recover-account/" + token,
    }

    email = EmailMessage('emails/recover_account.tpl', context, settings.EMAIL_HOST_USER, [user.email],
                         connection=connection)

    if not email.is_rendered:
        email.render()

    to_send.append(email)

    delivered = connection.send_messages(to_send)
    print("Successfully delivered {}/{} email to recover an account".format(delivered, len(to_send)))


# To be scheduled
def send_emails(frequency: MailNotificationFrequencies = MailNotificationFrequencies.DAILY):
    # Get all activated users who have their notifications frequency equals to the one of the scheduler's job
    users_conversations = User.objects.filter(is_active=True, mail_notif_freq_conversations=frequency)
    users_events = User.objects.filter(is_active=True, mail_notif_freq_events=frequency, ref_location__isnull=False)
    users_items = User.objects.filter(is_active=True, mail_notif_freq_items=frequency, ref_location__isnull=False)

    # Establish connection for the email sending
    connection = mail.get_connection(fail_silently=True)

    to_send = []
    to_send_types_count = {
        'conversations': 0,
        'items': 0,
        'events': 0
    }

    # Conversations: emails preparation
    for user in users_conversations:
        prepared_mail = _prepare_mail_notif_conversations(user, frequency, connection)
        if prepared_mail:
            to_send.append(prepared_mail)
            to_send_types_count['conversations'] += 1

    # Events: emails preparation
    for user in users_events:
        prepared_mail = _prepare_mail_notif_events(user, frequency, connection)
        if prepared_mail:
            to_send.append(prepared_mail)
            to_send_types_count['events'] += 1

    # Items: emails preparation
    for user in users_items:
        prepared_mail = _prepare_mail_notif_items(user, frequency, connection)
        if prepared_mail:
            to_send.append(prepared_mail)
            to_send_types_count['items'] += 1

    # Send list of prepared mails
    # https://docs.djangoproject.com/en/4.1/topics/email/#send-mass-mail
    # https://docs.djangoproject.com/en/4.1/topics/email/#send-mail
    # It uses EMAIL_* parameters from settings.py
    if len(to_send) > 0:
        delivered = connection.send_messages(to_send)
        print("Successfully delivered {}/{} emails:".format(delivered, len(to_send)))
        print("\t{} for conversations".format(to_send_types_count['conversations']))
        print("\t{} for events".format(to_send_types_count['events']))
        print("\t{} for items".format(to_send_types_count['items']))
    else:
        print("No scheduled emails to send.")


def start_mail_scheduler():
    def _scheduler_listener(event):
        if event.exception:
            print('The scheduled email sending crashed.')
        else:
            print('The scheduled email sending worked.')

    scheduler = BackgroundScheduler()

    # once a day: at 8 o'clock
    scheduler.add_job(send_emails, args=[MailNotificationFrequencies.DAILY], trigger='cron', hour=8)

    # once a week: every friday at 8 o'clock
    scheduler.add_job(send_emails, args=[MailNotificationFrequencies.WEEKLY], trigger='cron', day_of_week='fri', hour=8)

    # To test quickly (10s delay between checks), uncomment line below.
    # Update args parameter to tell who are the job's targets
    # MailNotificationFrequencies.DAILY = all users that have at least one of the 3 notif settings set on Daily
    # scheduler.add_job(send_emails, args=[MailNotificationFrequencies.DAILY], trigger='interval', seconds=10)

    scheduler.add_listener(_scheduler_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

    scheduler.start()
