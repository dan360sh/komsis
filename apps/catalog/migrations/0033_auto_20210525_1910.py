# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2021-05-25 16:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0032_auto_20210525_1219'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pricetype',
            options={'verbose_name': 'Тип цены', 'verbose_name_plural': 'Типы цен'},
        ),
    ]
