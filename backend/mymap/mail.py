from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
from apscheduler.schedulers.background import BackgroundScheduler
from django.core import mail
from django.contrib.auth import get_user_model
from django.db.models import Q, F
from django.conf import settings
from datetime import datetime, timedelta
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point

from mail_templated import EmailMessage

from .models import Message, MailNotificationFrequencies, MailNotificationFrequenciesOSM
from .models import Item

from djoser import email

import overpy

User = get_user_model()

# Time required between two conversation messages to be
# considered new and sending an email notification (in minutes)
delay_instant_notif_conversations = 10

to_show = {
    'conversations': 3,
    'items': 5,
    'events': 3,
    'osm': 20,
}

item_types = {
    "DN": "Donation",
    "LN": "Loan",
    "RQ": "Request",
    "EV": "Event"
}

class ActivationEmail(email.ActivationEmail):
    template_name = 'emails/activation.html'

class ConfirmationEmail(email.ConfirmationEmail):
    template_name = 'emails/confirmation.html'
    
def _get_unread_messages(user):
    messages = Message.objects.filter(conversation__users__user=user, seen=False).exclude(user=user)
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


def _prepare_mail_notif_norefloc(user, frequency: MailNotificationFrequencies, connection):
    context = {
            "user": user,
            "app_url": settings.APP_URL,
            "app_url_reflocsettings": settings.APP_URL+"/settings/notifications"
        }

    email = EmailMessage(
            'emails/notif_norefloc.tpl',
            context,
            settings.EMAIL_HOST_USER,
            [user.email],
            connection=connection
    )

    if not email.is_rendered:
        email.render()

    return email


def _get_osm_type(node):
    amenity = node.tags.get("amenity","");
    social_facility = node.tags.get("social_facility","");
    emergency = node.tags.get("emergency","");
    if amenity:
        return amenity
    elif social_facility:
        return social_facility
    elif emergency:
        return emergency
    else:
        return ""
    

def _get_last_new_osm_items_near_user(user, frequency: MailNotificationFrequenciesOSM):
    end = datetime.now().date()
    if frequency == MailNotificationFrequenciesOSM.DAILY:
        start = end - timedelta(days=1)   
    elif frequency == MailNotificationFrequenciesOSM.WEEKLY:
        start = end - timedelta(days=7)
    elif frequency == MailNotificationFrequenciesOSM.MONTHLY:
        start = end - timedelta(days=30)
    else:
        return [], 0
    start = "%sT00:00:00Z" % (start)
        
    overapi = overpy.Overpass()

    print(user)

    #overpass query to get nodes around reference location that were created since start date (and modified less than 5 times), limits the output to a maximum of to_show
    result = overapi.query(
        f"""
        ( 
          node["amenity"="public_bookcase"](around:{user.dwithin_notifications*1000},{user.ref_location.coords[1]},{user.ref_location.coords[0]})(newer:"{start}")(if:version() < 5);
          node["amenity"="give_box"](around:{user.dwithin_notifications*1000},{user.ref_location.coords[1]},{user.ref_location.coords[0]})(newer:"{start}")(if:version() < 5);
          node["amenity"="food_sharing"](around:{user.dwithin_notifications*1000},{user.ref_location.coords[1]},{user.ref_location.coords[0]})(newer:"{start}")(if:version() < 5);
          node["amenity"="freeshop"](around:{user.dwithin_notifications*1000},{user.ref_location.coords[1]},{user.ref_location.coords[0]})(newer:"{start}")(if:version() < 5);
          node["social_facility"="food_bank"](around:{user.dwithin_notifications*1000},{user.ref_location.coords[1]},{user.ref_location.coords[0]})(newer:"{start}")(if:version() < 5);
          node["social_facility"="soup_kitchen"](around:{user.dwithin_notifications*1000},{user.ref_location.coords[1]},{user.ref_location.coords[0]})(newer:"{start}")(if:version() < 5);
          node["amenity"="drinking_water"](around:{user.dwithin_notifications*1000},{user.ref_location.coords[1]},{user.ref_location.coords[0]})(newer:"{start}")(if:version() < 5);
          node["emergency"="defibrillator"](around:{user.dwithin_notifications*1000},{user.ref_location.coords[1]},{user.ref_location.coords[0]})(newer:"{start}")(if:version() < 5);
        );
        out {to_show['osm']} body qt;
        """
        )

    #node["amenity"="public_bookcase"](around:{user.dwithin_notifications*1000},{user.ref_location.coords[1]},{user.ref_location.coords[0]})(newer:"{start}")(if:version() < 5);

    
    #build array with essential node info for email
    nodes  = []
    nodes += [[ _get_osm_type(node), node.tags.get("name",""),
               Point(user.ref_location.coords[1],user.ref_location.coords[0]).distance(Point(float(node.lat),float(node.lon)))*100,
               float(node.lat), float(node.lon)]
           for node in result.nodes]
    sorted_nodes = sorted(nodes, key=lambda x: (x[0], x[2]))
    #print(sorted_nodes)
    return sorted_nodes,len(sorted_nodes)



def _prepare_mail_notif_osm(user, frequency: MailNotificationFrequencies, connection):
    new_items, n = _get_last_new_osm_items_near_user(user, frequency)
    if n > 0:
        print("we have to send an email with new osm items")
        if frequency == MailNotificationFrequenciesOSM.DAILY:
            digest = "Daily public resources digest"
        elif frequency == MailNotificationFrequenciesOSM.WEEKLY:
            digest = "Weekly public resources digest"
        elif frequency == MailNotificationFrequenciesOSM.MONTHLY:
            digest = "Monthly public resources digest"
        else:
            digest = "Recent items"
        context = {
            "n": n,
            "digest": digest,
            "user": user,
            "new_items": new_items,
            "app_url": settings.APP_URL,
            "to_show": to_show['osm']
        }

        email = EmailMessage(
            'emails/notif_digest_osm_items.tpl',
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


def send_mail_start_delete_account_process(user, token):
    connection = mail.get_connection(fail_silently=True)
    to_send = []

    context = {
        "user": user,
        "delete_account_token_url": settings.APP_URL + "/delete-account/" + token,
    }

    email = EmailMessage('emails/start_delete_account_process.tpl', context, settings.EMAIL_HOST_USER, [user.email],
                         connection=connection)

    if not email.is_rendered:
        email.render()

    to_send.append(email)

    delivered = connection.send_messages(to_send)
    print("Successfully delivered {}/{} email to start a delete account process".format(delivered, len(to_send)))

    
# To be scheduled
def send_emails(frequency: MailNotificationFrequencies = MailNotificationFrequencies.DAILY):
    # Get all activated users who have their notifications frequency equals to the one of the scheduler's job
    users_conversations = User.objects.filter(is_active=True, mail_notif_freq_conversations=frequency)
    users_events = User.objects.filter(is_active=True, mail_notif_freq_events=frequency, ref_location__isnull=False)
    users_items = User.objects.filter(is_active=True, mail_notif_freq_items=frequency, ref_location__isnull=False)
    #Get users who did/not configure ref location
    users_osm_withref = User.objects.filter(is_active=True, mail_notif_freq_osm=frequency, ref_location__isnull=False)
    users_withoutref = User.objects.filter(is_active=True, ref_location__isnull=True, mail_notif_generalinfo=True)
    
    # Establish connection for the email sending
    connection = mail.get_connection(fail_silently=True)

    to_send = []
    to_send_types_count = {
        'conversations': 0,
        'items': 0,
        'events': 0,
        'norefloc': 0,
        'osm': 0
    }

    # General information / no ref location: emails preparation
    # Runs only monthly for users with general info ON
    if frequency == 'M':
        for user in users_withoutref:
            prepared_mail = _prepare_mail_notif_norefloc(user, frequency, connection)
            if prepared_mail:
                to_send.append(prepared_mail)
                to_send_types_count['norefloc'] += 1

    #OSM public resources: emails preparation
    for user in users_osm_withref:
        prepared_mail = _prepare_mail_notif_osm(user, frequency, connection)
        if prepared_mail:
            to_send.append(prepared_mail)
            to_send_types_count['osm'] += 1

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
        print("\t{} for missing reference location".format(to_send_types_count['norefloc']))
        print("\t{} for OSM resources".format(to_send_types_count['osm']))
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
    
    # once a month: every last day of the month at 8 o'clock (for OSM and norefloc notifications)
    scheduler.add_job(send_emails, args=[MailNotificationFrequenciesOSM.MONTHLY], trigger='cron', month='*', day='last', hour=8)
    
    # To test quickly (10s delay between checks), uncomment line below.
    # Update args parameter to tell who are the job's targets
    # MailNotificationFrequencies.DAILY = all users that have at least one of the 3 notif settings set on Daily
    #scheduler.add_job(send_emails, args=[MailNotificationFrequencies.WEEKLY], trigger='interval', seconds=10)
    #scheduler.add_job(send_emails, args=[MailNotificationFrequenciesOSM.MONTHLY], trigger='interval', seconds=10)

    scheduler.add_listener(_scheduler_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

    scheduler.start()

