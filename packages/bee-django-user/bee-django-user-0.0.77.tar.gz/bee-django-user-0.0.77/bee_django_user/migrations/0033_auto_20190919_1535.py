# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2019-09-19 07:35
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('bee_django_user', '0032_userclass_lecturer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userleaverecord',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 9, 19, 7, 35, 43, 378032, tzinfo=utc)),
        ),
    ]
