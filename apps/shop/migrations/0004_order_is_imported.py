# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2020-07-27 13:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20200630_1703'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_imported',
            field=models.BooleanField(default=False, editable=False, verbose_name='Загружены в 1С'),
        ),
    ]
