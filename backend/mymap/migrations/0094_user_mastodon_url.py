# Generated by Django 3.2.23 on 2024-02-09 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mymap', '0093_auto_20231113_1533'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='mastodon_url',
            field=models.URLField(blank=True, default=''),
        ),
    ]