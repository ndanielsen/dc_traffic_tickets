# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-15 01:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20161028_0314'),
    ]

    operations = [
        migrations.AddField(
            model_name='freeformblogpage',
            name='in_blog_index',
            field=models.BooleanField(default=True, verbose_name='Include in Blog Index'),
        ),
    ]
