# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2021-04-30 11:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0026_auto_20210323_1635'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='display_nested_filters',
            field=models.BooleanField(default=False, verbose_name='Отображать в фильтрах первого уровня'),
        ),
    ]
