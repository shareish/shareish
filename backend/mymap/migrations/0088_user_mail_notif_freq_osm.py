# Generated by Django 3.2.10 on 2023-09-19 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mymap', '0087_item_closed_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='mail_notif_freq_osm',
            field=models.CharField(choices=[('D', 'Daily'), ('W', 'Weekly'), ('M', 'Monthly'), ('N', 'Never')], default='W', max_length=1),
        ),
    ]