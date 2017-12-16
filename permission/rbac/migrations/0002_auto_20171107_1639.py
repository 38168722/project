# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-07 08:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='permission',
            options={'verbose_name_plural': '权限表'},
        ),
        migrations.AlterField(
            model_name='permission',
            name='title',
            field=models.CharField(max_length=182, verbose_name='标题'),
        ),
        migrations.AlterField(
            model_name='permission',
            name='url',
            field=models.CharField(max_length=182, verbose_name='含正则的url'),
        ),
    ]