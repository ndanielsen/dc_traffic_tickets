# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-23 20:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_auto_20160923_1922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parkingviolationfine',
            name='code',
            field=models.CharField(db_index=True, max_length=10, null=True),
        ),
    ]
