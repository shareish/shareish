from django.db import models, migrations
import django_cryptography.fields

def forwards_copy_data(apps, schema_editor):
    User = apps.get_model("mymap", "User")
    
    for row in User.objects.all():
        row.first_name = row.old_first_name
        row.save(update_fields=["first_name"])


def reverse_copy_data(apps, schema_editor):
    User = apps.get_model("mymap", "User")
    
    for row in User.objects.all():
        row.old_first_name = row.first_name
        row.save(update_fields=["old_first_name"])


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
    ]