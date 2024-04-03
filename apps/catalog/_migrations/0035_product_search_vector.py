# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2020-03-18 06:31
from __future__ import unicode_literals

import django.contrib.postgres.search
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0034_auto_20200317_1742'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='search_vector',
            field=django.contrib.postgres.search.SearchVectorField(null=True, verbose_name='вектор поиска'),
        ),
    ]
