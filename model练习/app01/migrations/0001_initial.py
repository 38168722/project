# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-29 08:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='部门名称')),
            ],
            options={
                'verbose_name': '部门表',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='角色')),
            ],
            options={
                'verbose_name': '角色',
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='用户名')),
                ('password', models.CharField(max_length=32, verbose_name='密码')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Department', verbose_name='部门')),
                ('role', models.ManyToManyField(to='app01.Role', verbose_name='角色')),
            ],
            options={
                'verbose_name': '用户表',
            },
        ),
    ]
