# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-18 10:21
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ebs', '0004_auto_20170418_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='published',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 18, 10, 21, 40, 996950, tzinfo=utc)),
        ),
    ]
