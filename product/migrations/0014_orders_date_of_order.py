# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-30 09:57
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0013_auto_20160530_0749'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='date_of_order',
            field=models.TimeField(default=datetime.datetime(2016, 1, 1, 0, 0)),
        ),
    ]
