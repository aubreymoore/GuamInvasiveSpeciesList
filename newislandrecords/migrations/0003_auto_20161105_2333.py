# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-05 23:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newislandrecords', '0002_auto_20161105_1232'),
    ]

    operations = [
        migrations.AddField(
            model_name='newislandrecord',
            name='created',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='newislandrecord',
            name='created_by',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='newislandrecord',
            name='update_by',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='newislandrecord',
            name='updated',
            field=models.DateTimeField(null=True),
        ),
    ]
