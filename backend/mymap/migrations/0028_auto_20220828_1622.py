# Generated by Django 3.2.10 on 2022-08-28 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mymap', '0027_alter_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='up2date_buyer',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='conversation',
            name='up2date_owner',
            field=models.BooleanField(default=True),
        ),
    ]
