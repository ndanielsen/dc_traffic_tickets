# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-01 19:33
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_auto_20161001_1502'),
    ]

    operations = [
        migrations.AddField(
            model_name='parkingviolationfine',
            name='compiled_ticket_descriptions',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={'empty': True}),
            preserve_default=False,
        ),
    ]
