# Generated by Django 3.2.10 on 2022-07-06 10:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mymap', '0006_barter_in_progress'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='barter',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='barterimage',
            options={'ordering': ['barter']},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['sign_in_date']},
        ),
        migrations.AlterField(
            model_name='barterimage',
            name='barter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='mymap.barter'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
