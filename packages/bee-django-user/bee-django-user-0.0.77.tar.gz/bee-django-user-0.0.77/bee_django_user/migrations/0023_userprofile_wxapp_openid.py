# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2019-06-21 14:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bee_django_user', '0022_auto_20190612_1746'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='wxapp_openid',
            field=models.CharField(blank=True, max_length=180, null=True, verbose_name='\u5fae\u4fe1\u5c0f\u7a0b\u5e8fopen id'),
        ),
    ]
