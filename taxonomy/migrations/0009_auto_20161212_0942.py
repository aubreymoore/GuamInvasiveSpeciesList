# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-11 23:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0008_remove_upload_dwca_uploaded_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='upload_dwca',
            old_name='document',
            new_name='dwca',
        ),
    ]
