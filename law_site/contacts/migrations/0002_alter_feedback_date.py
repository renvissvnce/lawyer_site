# Generated by Django 3.2.5 on 2021-11-15 12:04

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 11, 15, 12, 4, 26, 951010, tzinfo=utc)),
        ),
    ]
