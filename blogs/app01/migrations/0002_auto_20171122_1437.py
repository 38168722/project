# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-22 06:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteArticleCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='SiteCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.AlterModelOptions(
            name='articleup',
            options={'verbose_name_plural': '文章点赞表'},
        ),
        migrations.AlterModelOptions(
            name='commentup',
            options={'verbose_name_plural': '评论点赞表'},
        ),
        migrations.AlterModelOptions(
            name='userfans',
            options={'verbose_name_plural': '粉丝表'},
        ),
        migrations.RemoveField(
            model_name='article',
            name='article_type_id',
        ),
        migrations.AddField(
            model_name='sitearticlecategory',
            name='site_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.SiteCategory'),
        ),
        migrations.AddField(
            model_name='article',
            name='site_article_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.SiteArticleCategory'),
        ),
    ]
