# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2021-11-29 16:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0037_auto_20210913_1553'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='tech_price',
            field=models.FloatField(default=0, verbose_name='Техническая цена для товара'),
        ),
    ]
