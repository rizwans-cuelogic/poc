# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-20 12:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ebs', '0011_auto_20170420_1751'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='categories',
        ),
        migrations.RemoveField(
            model_name='blog',
            name='organisation',
        ),
        migrations.RemoveField(
            model_name='blogfile',
            name='blog',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='blog',
        ),
        migrations.DeleteModel(
            name='Blog',
        ),
        migrations.DeleteModel(
            name='BlogFile',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
