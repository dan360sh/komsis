# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2020-11-23 11:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slider',
            name='link',
            field=models.CharField(blank=True, default='', max_length=10000, verbose_name='Ссылка'),
        ),
    ]
