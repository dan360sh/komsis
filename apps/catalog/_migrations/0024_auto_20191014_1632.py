# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-10-14 13:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0023_auto_20191014_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='option',
            name='count',
            field=models.FloatField(blank=True, default=0, verbose_name='Количество'),
        ),
    ]
