# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2020-12-26 09:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0022_product_vector'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='title_upper',
            field=models.CharField(blank=True, db_index=True, max_length=3000, null=True, verbose_name='Наименование UPPER'),
        ),
    ]