# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-05 23:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newislandrecords', '0004_auto_20161105_2340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newislandrecord',
            name='update_by',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='newislandrecord',
            name='updated',
            field=models.DateField(blank=True, null=True),
        ),
    ]
