# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-01 14:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_auto_20160927_0009'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='parkingviolation',
            index_together=set([]),
        ),
        migrations.RemoveField(
            model_name='parkingviolation',
            name='address_id',
        ),
        migrations.RemoveField(
            model_name='parkingviolation',
            name='body_style',
        ),
        migrations.RemoveField(
            model_name='parkingviolation',
            name='filename',
        ),
        migrations.RemoveField(
            model_name='parkingviolation',
            name='rp_plate_state',
        ),
        migrations.RemoveField(
            model_name='parkingviolation',
            name='streetsegid',
        ),
        migrations.RemoveField(
            model_name='parkingviolation',
            name='violation_code',
        ),
    ]
