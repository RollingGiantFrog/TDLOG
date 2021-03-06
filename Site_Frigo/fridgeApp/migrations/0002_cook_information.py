# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-27 19:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fridgeApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cook_information',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cook_time', models.FloatField()),
                ('cook_time_unit', models.CharField(max_length=30)),
                ('rest_time', models.FloatField()),
                ('rest_time_unit', models.CharField(max_length=30)),
                ('preparation_time', models.FloatField()),
                ('preparation_time_unit', models.CharField(max_length=30)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fridgeApp.Recipe')),
            ],
        ),
    ]
