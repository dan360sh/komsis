# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2021-06-29 08:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0019_auto_20210531_1412'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='valid_phone',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Проверенный номер телефона'),
        ),
    ]
