# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-20 10:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ebs', '0002_auto_20170418_1643'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forgotpassword',
            name='username',
        ),
        migrations.DeleteModel(
            name='forgotpassword',
        ),
    ]
