# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-11 22:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0005_auto_20161205_2133'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dwca',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.FileField(upload_to='dwca/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
