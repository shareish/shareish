# Manually created by Florent Banneux on 2023-04-14 13:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

from mymap.models import UserMapExtraCategories


def forwards_func(apps, schema_editor):
    UserMapExtraCategory = apps.get_model("mymap", "UserMapExtraCategory")
    User = apps.get_model("mymap", "User")
    db_alias = schema_editor.connection.alias
    users = User.objects.all()
    for user in users:
        for category in UserMapExtraCategories:
            UserMapExtraCategory.objects.using(db_alias).create(user=user, category=category)


def reverse_func(apps, schema_editor):
    UserMapExtraCategory = apps.get_model("mymap", "UserMapExtraCategory")
    db_alias = schema_editor.connection.alias
    UserMapExtraCategory.objects.using(db_alias).all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('mymap', '0069_remove_item_in_progress'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserMapExtraCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('BKC', 'Public bookcases'), ('DEF', 'Defibrillators'), ('DWS', 'Drinking water spots'), ('FDB', 'Food Banks'), ('FDS', 'Food Sharing'), ('FLF', 'Falling fruits'), ('FRS', 'Free shops'), ('GVB', 'Give boxes'), ('SPK', 'Soup Kitchens')], max_length=3)),
                ('selected', models.BooleanField(default=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['user_id', 'category'],
            },
        ),
        migrations.RemoveConstraint(
            model_name='itemview',
            name='unique__mymap_itemviews__item_user',
        ),
        migrations.AddConstraint(
            model_name='itemview',
            constraint=models.UniqueConstraint(fields=('item', 'user'), name='unique__mymap_itemview__item_user'),
        ),
        migrations.AddField(
            model_name='usermapextracategory',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='map_ecats', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='usermapextracategory',
            constraint=models.UniqueConstraint(fields=('user', 'category'), name='unique__mymap_usermapextracategory__user_category'),
        ),
        migrations.RunPython(forwards_func, reverse_func)
    ]
