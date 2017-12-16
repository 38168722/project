# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-07 08:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=182, verbose_name='标题')),
                ('title', models.CharField(max_length=182, verbose_name='含正则的url')),
                ('is_menu', models.BooleanField(verbose_name='是否是菜单')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32)),
                ('permissions', models.ManyToManyField(blank=True, to='rbac.Permission', verbose_name='具有的所有权限')),
            ],
            options={
                'verbose_name_plural': '角色表',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=182, verbose_name='用户名')),
                ('password', models.CharField(max_length=182, verbose_name='密码')),
                ('email', models.CharField(max_length=32, verbose_name='邮箱')),
                ('roles', models.ManyToManyField(blank=True, to='rbac.Role', verbose_name='具有的所有角色')),
            ],
            options={
                'verbose_name_plural': '用户表',
            },
        ),
    ]