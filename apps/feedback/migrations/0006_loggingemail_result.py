# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2021-08-13 12:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0005_auto_20210813_1440'),
    ]

    operations = [
        migrations.AddField(
            model_name='loggingemail',
            name='result',
            field=models.TextField(blank=True, null=True, verbose_name='Отчет об отправке'),
        ),
    ]
