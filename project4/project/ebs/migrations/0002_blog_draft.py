# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-17 10:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='Draft',
            field=models.BooleanField(default=False),
        ),
    ]
