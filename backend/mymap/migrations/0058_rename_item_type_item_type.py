# Generated by Django 3.2.10 on 2023-03-16 13:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mymap', '0057_auto_20230316_1405'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='item_type',
            new_name='type',
        ),
    ]