# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2021-05-27 11:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_account_discount_card'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discountcard',
            name='id_1c',
            field=models.CharField(max_length=200, unique=True, verbose_name='ИД из 1с'),
        ),
    ]
