# Generated by Django 3.2.10 on 2023-03-04 16:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mymap', '0051_alter_item_item_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='creationdate',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
