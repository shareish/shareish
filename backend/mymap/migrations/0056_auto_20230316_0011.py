# Generated by Django 3.2.10 on 2023-03-15 23:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mymap', '0055_auto_20230311_1434'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='itemimage',
            options={'ordering': ['item_id', 'position']},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['sign_up_date', 'id']},
        ),
        migrations.AlterModelOptions(
            name='userimage',
            options={'ordering': ['user_id', '-id']},
        ),
    ]