# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2021-05-24 10:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_auto_20210513_0934'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='price_type',
            field=models.CharField(choices=[('a6bfe5d1-ccce-11dd-8d29-001fc6b4b87e', 'Розница'), ('a6bfe5d2-ccce-11dd-8d29-001fc6b4b87e', 'Оптовая')], default='a6bfe5d1-ccce-11dd-8d29-001fc6b4b87e', max_length=150, verbose_name='Отображаемый тип цены'),
        ),
    ]
