# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-16 10:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0022_auto_20160616_1002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_stars',
            field=models.CharField(default='', max_length=5),
        ),
    ]
