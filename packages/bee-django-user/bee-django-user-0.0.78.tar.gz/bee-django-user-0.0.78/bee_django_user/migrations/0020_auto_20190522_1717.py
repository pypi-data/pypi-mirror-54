# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2019-05-22 09:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bee_django_user', '0019_auto_20190522_1642'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usersn',
            options={'ordering': ['start']},
        ),
        migrations.AlterModelTable(
            name='usersn',
            table='bee_django_user_sn',
        ),
    ]
