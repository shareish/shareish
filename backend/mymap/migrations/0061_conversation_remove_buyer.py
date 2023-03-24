# Manually created by Florent Banneux on 2023-03-23 16:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mymap', '0060_conversation_starter_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conversation',
            name='buyer',
        ),
    ]
