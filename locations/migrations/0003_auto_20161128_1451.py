# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-28 04:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0002_auto_20161128_1435'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='date_modified',
        ),
        migrations.AddField(
            model_name='location',
            name='created_by',
            field=models.CharField(default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
    ]
