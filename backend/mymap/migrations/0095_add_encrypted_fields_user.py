from django.db import models, migrations
import django_cryptography.fields
import django.contrib.gis.db.models.fields
import django_cryptography.fields
from django.contrib.gis.db import models

FIELDS = ["first_name","last_name"]


def forwards_copy_data(apps, schema_editor):
    Model = apps.get_model("mymap", "User")

    for row in Model.objects.all():
        for field in FIELDS:
            setattr(row, field, getattr(row, "old_" + field))
        row.save()


def reverse_copy_data(apps, schema_editor):
    Model = apps.get_model("mymap", "User")

    for row in Model.objects.all():
        for field in FIELDS:
            setattr(row, "old_" + field, getattr(row, field))
        row.save()



class Migration(migrations.Migration):
     dependencies = [
         ('mymap', '0094_user_mastodon_url'),
     ]

     operations = [
         migrations.RenameField(
             model_name='user',
             old_name='first_name',
             new_name='old_first_name',
         ),

         migrations.AddField(
             model_name='user',
             name='first_name',
             field=django_cryptography.fields.encrypt(
                 models.CharField(max_length=50, null=True, blank=True)),
             preserve_default=False,
         ),

         migrations.RunPython(
             forwards_copy_data,
             reverse_copy_data
         ),

         migrations.RemoveField(
             model_name='user',
             name='old_first_name',
        ),

        #---------------------------------------------#

         migrations.RenameField(
             model_name='user',
             old_name='last_name',
             new_name='old_last_name',
         ),

         migrations.AddField(
             model_name='user',
             name='last_name',
             field=django_cryptography.fields.encrypt(
                 models.CharField(max_length=20, null=True, blank=True)),
             preserve_default=False,
         ),

         migrations.RunPython(
             forwards_copy_data,
             reverse_copy_data
         ),

         migrations.RemoveField(
             model_name='user',
             name='old_last_name',
        ),

        #---------------------------------------------#

     ]

