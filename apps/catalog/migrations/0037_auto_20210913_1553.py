# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2021-09-13 12:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0036_category_alt_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='alt_title',
            field=models.CharField(blank=True, help_text='Заголовок, который\n                                            будет выводиться на страницах,\n                                            прим. страница с направлениями', max_length=200, null=True, verbose_name='Альтернативное наименование'),
        ),
    ]
