# Generated by Django 3.2.10 on 2023-05-05 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mymap', '0081_alter_token_action'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='lifespan',
            field=models.DurationField(null=True),
        ),
        migrations.AlterField(
            model_name='token',
            name='used_at',
            field=models.DateTimeField(null=True),
        ),
    ]