from django.db import models, migrations
import django_cryptography.fields
import django.contrib.gis.db.models.fields
import django_cryptography.fields
from django.contrib.gis.db import models

FIELDS = ["content"]


def forwards_copy_data(apps, schema_editor):
    Model = apps.get_model("mymap", "Message")

    for row in Model.objects.all():
        for field in FIELDS:
            setattr(row, field, getattr(row, "old_" + field))
        row.save()


def reverse_copy_data(apps, schema_editor):
    Model = apps.get_model("mymap", "Message")

    for row in Model.objects.all():
        for field in FIELDS:
            setattr(row, "old_" + field, getattr(row, field))
        row.save()



class Migration(migrations.Migration):
     dependencies = [
         ('mymap', '0095_add_encrypted_fields_user'),
     ]

     operations = [
         migrations.RenameField(
             model_name='message',
             old_name='content',
             new_name='old_content',
         ),

         migrations.AddField(
             model_name='message',
             name='content',
             field=django_cryptography.fields.encrypt(models.TextField()),
             preserve_default=False,
         ),

         migrations.RunPython(
             forwards_copy_data,
             reverse_copy_data
         ),

         migrations.RemoveField(
             model_name='message',
             name='old_content',
        ),

        #---------------------------------------------#

     ]

