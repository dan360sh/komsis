# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-10-25 08:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0009_auto_20181025_1137'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='odnoklassniky',
            field=models.CharField(blank=True, max_length=300, verbose_name='Ссылка на Одноклассники'),
        ),
    ]
