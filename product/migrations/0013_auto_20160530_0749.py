# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-30 07:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0012_orders_orders_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_memory',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_orm',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_screen_resolution',
            field=models.CharField(max_length=20),
        ),
    ]
