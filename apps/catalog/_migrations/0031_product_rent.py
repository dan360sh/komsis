# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-12-23 09:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0030_brand_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='rent',
            field=models.BooleanField(default=False, verbose_name='Доступна аренда'),
        ),
    ]
