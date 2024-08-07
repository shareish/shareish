# Generated by Django 3.2.10 on 2023-01-07 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mymap', '0035_auto_20230104_1215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category1',
            field=models.CharField(choices=[('FD', 'Food and Supplies'), ('AN', 'Pets and Animals'), ('EN', 'Arts, Culture, and Entertainments'), ('CL', 'Collectors'), ('HL', 'Helping hand and Manual Labor'), ('AT', 'Administrative tasks'), ('DY', 'Do-it-Yourself'), ('BT', 'Beauty and Well-being'), ('HE', 'Health'), ('EY', 'Energy and Heating'), ('CH', 'Childhood'), ('CO', 'Clothes'), ('IT', 'Multimedia Hardware'), ('CS', 'Informatics Software'), ('GD', 'Gardening and Nature'), ('HS', 'Living spaces and Housing'), ('EQ', 'Tools and Ustensils'), ('HD', 'Holidays, Week-end, Leisures'), ('BK', 'Books, CDs and DVDs'), ('SP', 'Sports'), ('TS', 'Transportation, Delivery, Pick-up, Moving'), ('VE', 'Vehicles and Means of transport'), ('OT', 'Other')], default='OT', max_length=2),
        ),
        migrations.AlterField(
            model_name='item',
            name='category2',
            field=models.CharField(blank=True, choices=[('FD', 'Food and Supplies'), ('AN', 'Pets and Animals'), ('EN', 'Arts, Culture, and Entertainments'), ('CL', 'Collectors'), ('HL', 'Helping hand and Manual Labor'), ('AT', 'Administrative tasks'), ('DY', 'Do-it-Yourself'), ('BT', 'Beauty and Well-being'), ('HE', 'Health'), ('EY', 'Energy and Heating'), ('CH', 'Childhood'), ('CO', 'Clothes'), ('IT', 'Multimedia Hardware'), ('CS', 'Informatics Software'), ('GD', 'Gardening and Nature'), ('HS', 'Living spaces and Housing'), ('EQ', 'Tools and Ustensils'), ('HD', 'Holidays, Week-end, Leisures'), ('BK', 'Books, CDs and DVDs'), ('SP', 'Sports'), ('TS', 'Transportation, Delivery, Pick-up, Moving'), ('VE', 'Vehicles and Means of transport'), ('OT', 'Other')], max_length=2),
        ),
        migrations.AlterField(
            model_name='item',
            name='category3',
            field=models.CharField(blank=True, choices=[('FD', 'Food and Supplies'), ('AN', 'Pets and Animals'), ('EN', 'Arts, Culture, and Entertainments'), ('CL', 'Collectors'), ('HL', 'Helping hand and Manual Labor'), ('AT', 'Administrative tasks'), ('DY', 'Do-it-Yourself'), ('BT', 'Beauty and Well-being'), ('HE', 'Health'), ('EY', 'Energy and Heating'), ('CH', 'Childhood'), ('CO', 'Clothes'), ('IT', 'Multimedia Hardware'), ('CS', 'Informatics Software'), ('GD', 'Gardening and Nature'), ('HS', 'Living spaces and Housing'), ('EQ', 'Tools and Ustensils'), ('HD', 'Holidays, Week-end, Leisures'), ('BK', 'Books, CDs and DVDs'), ('SP', 'Sports'), ('TS', 'Transportation, Delivery, Pick-up, Moving'), ('VE', 'Vehicles and Means of transport'), ('OT', 'Other')], max_length=2),
        ),
    ]
