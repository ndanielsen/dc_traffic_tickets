# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-17 00:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20160505_1901'),
    ]

    operations = [
        migrations.RenameField(
            model_name='parkingviolation',
            old_name='location',
            new_name='point',
        ),
    ]
