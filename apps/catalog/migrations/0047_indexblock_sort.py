# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2022-02-28 11:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0046_indexblock_is_clickable'),
    ]

    operations = [
        migrations.AddField(
            model_name='indexblock',
            name='sort',
            field=models.IntegerField(default=1, verbose_name='Сортировка'),
        ),
    ]
