# Generated by Django 3.2.10 on 2023-04-03 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mymap', '0063_auto_20230328_1832'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='itemcomment',
            options={'ordering': ['-creationdate']},
        ),
    ]
