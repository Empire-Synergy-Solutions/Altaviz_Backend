# Generated by Django 3.0.4 on 2021-03-12 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waitinglist', '0002_auto_20160929_1624'),
    ]

    operations = [
        migrations.AddField(
            model_name='waitinglistentry',
            name='car_type',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='waitinglistentry',
            name='phone_number',
            field=models.CharField(blank=True, max_length=11),
        ),
    ]
