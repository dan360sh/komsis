# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2020-09-02 06:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0017_auto_20200828_1202'),
    ]

    operations = [
        migrations.AddField(
            model_name='attributesgroup',
            name='show_parent',
            field=models.BooleanField(default=True, verbose_name='Показывать в родительских категориях'),
        ),
    ]
