# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-27 19:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fridgeApp', '0003_auto_20161127_2012'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cook_information',
            old_name='information_time',
            new_name='time',
        ),
        migrations.RenameField(
            model_name='cook_information',
            old_name='information_time_unit',
            new_name='time_unit',
        ),
    ]
