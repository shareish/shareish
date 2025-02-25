# Manual migration to add REP usermapextracategory to existing users in database

from django.db import migrations, models
import django.db.models.deletion
from mymap.models import UserMapExtraCategories


def forwards_func(apps, schema_editor):
    UserMapExtraCategory = apps.get_model("mymap", "UserMapExtraCategory")
    User = apps.get_model("mymap", "User")
    db_alias = schema_editor.connection.alias
    users = User.objects.using(db_alias).all()
    for user in users:
        UserMapExtraCategory.objects.using(db_alias).create(user=user, category="REP")


def reverse_func(apps, schema_editor):
    UserMapExtraCategory = apps.get_model("mymap", "UserMapExtraCategory")
    db_alias = schema_editor.connection.alias
    UserMapExtraCategory.objects.using(db_alias).filter(category="REP").delete()
    

class Migration(migrations.Migration):

    dependencies = [
        ('mymap', '0095_alter_usermapextracategory_category'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func)
    ]
