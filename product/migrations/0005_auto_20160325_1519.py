# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-25 15:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_auto_20160325_1516'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='product_brend',
            new_name='product_brand',
        ),
    ]
