# Generated by Django 3.2.10 on 2022-04-04 14:16

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mymap', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barter',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, srid=4326),
        ),
    ]
