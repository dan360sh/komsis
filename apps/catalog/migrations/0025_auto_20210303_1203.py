# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2021-03-03 09:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0024_productstorage_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productstorage',
            name='address',
            field=models.CharField(blank=True, default='', max_length=127, verbose_name='Адрес'),
        ),
    ]
