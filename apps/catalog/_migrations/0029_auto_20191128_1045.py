# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-11-28 07:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0028_product_title_upper'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='brand',
            options={'ordering': ('sort',), 'verbose_name': 'производитель', 'verbose_name_plural': 'Производители'},
        ),
        migrations.AddField(
            model_name='brand',
            name='sort',
            field=models.PositiveIntegerField(default=500, verbose_name='Сортировка'),
        ),
    ]
