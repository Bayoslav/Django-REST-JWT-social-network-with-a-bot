# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-28 02:19
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_auto_20170828_0411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 28, 4, 19, 48, 592537)),
        ),
    ]
