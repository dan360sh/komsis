# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2022-01-19 14:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0014_contactemail'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactemail',
            name='show_city',
            field=models.BooleanField(default=False, verbose_name='Показывать город?'),
        ),
    ]