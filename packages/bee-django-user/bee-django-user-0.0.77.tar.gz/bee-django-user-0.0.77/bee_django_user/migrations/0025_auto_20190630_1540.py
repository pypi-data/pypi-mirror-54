# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2019-06-30 07:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bee_django_user', '0024_userparentrelation'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserParentRelation',
            new_name='UserProfileParentRelation',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='parents',
            field=models.ManyToManyField(through='bee_django_user.UserProfileParentRelation', to='bee_django_user.UserProfile'),
        ),
        migrations.AlterField(
            model_name='userprofileparentrelation',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent', to='bee_django_user.UserProfile', verbose_name='\u5bb6\u957f'),
        ),
        migrations.AlterField(
            model_name='userprofileparentrelation',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student', to='bee_django_user.UserProfile', verbose_name='\u5b66\u751f'),
        ),
    ]
