# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2021-11-30 17:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0009_auto_20211010_1137'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='time_work_cherep',
            field=models.CharField(blank=True, default='', max_length=300, verbose_name='Режи работы, Череповец'),
        ),
    ]