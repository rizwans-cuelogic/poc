# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-20 12:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ebs', '0008_forgotpassword'),
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
