# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-14 03:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0012_auto_20161214_1312'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dwcadistribution',
            old_name='xuuid',
            new_name='uuid',
        ),
    ]
