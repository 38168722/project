# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-29 08:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.Department', verbose_name='部门'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='role',
            field=models.ManyToManyField(blank=True, null=True, to='app01.Role', verbose_name='角色'),
        ),
    ]
