# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-14 03:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0011_dwcadistribution_dwcaresourcerelationship_dwcavernacular'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dwcadistribution',
            old_name='uuid',
            new_name='xuuid',
        ),
    ]