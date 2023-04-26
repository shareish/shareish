# Manually created by Florent Banneux on 2023-04-17 14:26

from django.contrib.gis.geos import Point
from django.db import migrations


def reverse_coords(apps, schema_editor):
    Item = apps.get_model("mymap", "Item")
    User = apps.get_model("mymap", "User")
    db_alias = schema_editor.connection.alias

    items = Item.objects.using(db_alias).filter(location__isnull=False)
    for item in items:
        pt = item.location
        item.location = Point(pt.y, pt.x, srid=4326)
        item.save()

    users = User.objects.using(db_alias).filter(ref_location__isnull=False)
    for user in users:
        pt = user.ref_location
        user.ref_location = Point(pt.y, pt.x, srid=4326)
        user.save()


def forwards_func(apps, schema_editor):
    reverse_coords(apps, schema_editor)


def reverse_func(apps, schema_editor):
    reverse_coords(apps, schema_editor)


class Migration(migrations.Migration):
    dependencies = [
        ('mymap', '0071_save_item_viewing'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func)
    ]
