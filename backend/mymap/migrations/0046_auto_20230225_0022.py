# Generated by Django 3.2.10 on 2023-02-24 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mymap', '0045_item_creationdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='mail_notif_freq_conversations',
            field=models.CharField(choices=[('I', 'Instantly'), ('D', 'Daily'), ('N', 'Never')], default='I', max_length=1),
        ),
        migrations.AddField(
            model_name='user',
            name='mail_notif_freq_events',
            field=models.CharField(choices=[('I', 'Instantly'), ('D', 'Daily'), ('W', 'Weekly'), ('N', 'Never')], default='D', max_length=1),
        ),
        migrations.AddField(
            model_name='user',
            name='mail_notif_freq_items',
            field=models.CharField(choices=[('I', 'Instantly'), ('D', 'Daily'), ('W', 'Weekly'), ('N', 'Never')], default='D', max_length=1),
        ),
    ]