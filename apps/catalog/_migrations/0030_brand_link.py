# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-12-03 11:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0029_auto_20191128_1045'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='link',
            field=models.CharField(blank=True, default='', max_length=127, verbose_name='Ссылка'),
        ),
    ]
