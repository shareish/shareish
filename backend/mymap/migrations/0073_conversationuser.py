# Generated by Django 3.2.10 on 2023-04-26 13:57
# Manually updated by Florent Banneux

from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


def forwards_func(apps, schema_editor):
    Conversation = apps.get_model("mymap", "Conversation")
    ConversationUser = apps.get_model("mymap", "ConversationUser")
    Message = apps.get_model("mymap", "Message")
    db_alias = schema_editor.connection.alias

    conversations = Conversation.objects.using(db_alias).all()
    for conversation in conversations:
        first_message = Message.objects.using(db_alias).filter(conversation=conversation).order_by('date').first()
        if first_message is not None:
            ConversationUser.objects.using(db_alias).create(
                conversation=conversation,
                user=conversation.starter,
                joining_date=first_message.date,
                created_date=first_message.date
            )
            ConversationUser.objects.using(db_alias).create(
                conversation=conversation,
                user=conversation.item.user,
                joining_date=first_message.date,
                created_date=first_message.date
            )


def reverse_func(apps, schema_editor):
    ConversationUser = apps.get_model("mymap", "ConversationUser")
    db_alias = schema_editor.connection.alias
    ConversationUser.objects.using(db_alias).all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('mymap', '0072_invert_coords'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConversationUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('joining_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('conversation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='mymap.conversation')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conversations_link', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RunPython(forwards_func, reverse_func),
        migrations.RemoveField(
            model_name='conversation',
            name='starter',
        ),
    ]
