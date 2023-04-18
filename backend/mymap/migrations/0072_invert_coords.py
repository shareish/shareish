# Manually created by Florent Banneux on 2023-04-17 14:26

from django.contrib.gis.geos import Point
from django.db import migrations

from mymap.models import Item, User


def reverse_coords():
    items = Item.objects.filter(location__isnull=False)
    for item in items:
        pt = item.location
        item.location = Point(pt.y, pt.x, srid=4326)
        item.save()

    users = User.objects.filter(ref_location__isnull=False)
    for user in users:
        pt = user.ref_location
        user.ref_location = Point(pt.y, pt.x, srid=4326)
        user.save()


def forwards_func(apps, schema_editor):
    reverse_coords()


def reverse_func(apps, schema_editor):
    reverse_coords()


class Migration(migrations.Migration):
    dependencies = [
        ('mymap', '0071_save_item_viewing'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func)
    ]
