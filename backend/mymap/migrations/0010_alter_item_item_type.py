# Generated by Django 3.2.10 on 2022-07-15 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mymap', '0009_auto_20220713_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='item_type',
            field=models.CharField(choices=[('DN', 'Donation'), ('LN', 'Loan'), ('BR', 'Request')], default='BR', max_length=2),
        ),
    ]
