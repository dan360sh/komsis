# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-10-25 05:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0004_auto_20181025_0836'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='color_scheme_alpha',
            field=models.CharField(blank=True, max_length=20, verbose_name='Цветовая схема c alpha'),
        ),
    ]