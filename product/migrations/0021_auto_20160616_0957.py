# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-16 09:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0020_comments_name_of_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='users_liked',
            new_name='users_voted',
        ),
        migrations.AddField(
            model_name='product',
            name='product_stars',
            field=models.IntegerField(default=0),
        ),
    ]
