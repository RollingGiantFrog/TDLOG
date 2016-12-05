# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-27 19:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fridgeApp', '0002_cook_information'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cook_information',
            old_name='cook_time',
            new_name='information_time',
        ),
        migrations.RenameField(
            model_name='cook_information',
            old_name='cook_time_unit',
            new_name='information_time_unit',
        ),
        migrations.RemoveField(
            model_name='cook_information',
            name='preparation_time',
        ),
        migrations.RemoveField(
            model_name='cook_information',
            name='preparation_time_unit',
        ),
        migrations.RemoveField(
            model_name='cook_information',
            name='rest_time',
        ),
        migrations.RemoveField(
            model_name='cook_information',
            name='rest_time_unit',
        ),
        migrations.AddField(
            model_name='cook_information',
            name='information_text',
            field=models.CharField(default='information', max_length=200),
            preserve_default=False,
        ),
    ]