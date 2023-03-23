# Manually created by Florent Banneux on 2023-03-23 16:09

from django.db import migrations
from django.db.models import F


def forwards_func(apps, schema_editor):
    Conversation = apps.get_model("mymap", "Conversation")
    db_alias = schema_editor.connection.alias
    Conversation.objects.using(db_alias).update(starter_id=F('buyer_id'))

def reverse_func(apps, schema_editor):
    Conversation = apps.get_model("mymap", "Conversation")
    db_alias = schema_editor.connection.alias
    Conversation.objects.using(db_alias).update(buyer_id=F('starter_id'))

class Migration(migrations.Migration):

    dependencies = [
        ('mymap', '0059_auto_20230323_1709'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
        migrations.RemoveField(
            model_name='conversation',
            name='buyer',
        ),
    ]
