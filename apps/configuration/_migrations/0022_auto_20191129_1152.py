# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-11-29 08:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0021_slider'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='slider',
            options={'ordering': ['sort'], 'verbose_name': 'Элемент слайдера', 'verbose_name_plural': 'Слайдер'},
        ),
        migrations.AddField(
            model_name='slider',
            name='sort',
            field=models.PositiveIntegerField(default=500, verbose_name='Сортировка'),
        ),
    ]
