# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-28 01:03
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('text', models.CharField(max_length=1000)),
                ('date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.AlterModelOptions(
            name='user',
            options={},
        ),
        migrations.RemoveField(
            model_name='user',
            name='enrichjson',
        ),
        migrations.AddField(
            model_name='user',
            name='enrich_json',
            field=models.CharField(default='', max_length=8000),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 28, 3, 3, 42, 32392)),
        ),
        migrations.AddField(
            model_name='post',
            name='creator',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='likers',
            field=models.ManyToManyField(related_name='likerslist', to=settings.AUTH_USER_MODEL),
        ),
    ]
