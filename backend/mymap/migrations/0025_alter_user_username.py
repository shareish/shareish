# Generated by Django 3.2.10 on 2022-08-18 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mymap', '0024_auto_20220818_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]