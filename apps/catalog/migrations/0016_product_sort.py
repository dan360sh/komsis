# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2020-08-21 09:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0015_auto_20200720_1150'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sort',
            field=models.IntegerField(default='999999999', verbose_name='Приоритет'),
        ),
    ]
