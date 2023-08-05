# Generated by Django 2.1.8 on 2019-07-04 13:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='events',
            name='event_date_time',
        ),
        migrations.RemoveField(
            model_name='events',
            name='sort_order',
        ),
        migrations.AddField(
            model_name='events',
            name='entry_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 4, 13, 38, 8, 803814), verbose_name='Entry Date'),
            preserve_default=False,
        ),
    ]
