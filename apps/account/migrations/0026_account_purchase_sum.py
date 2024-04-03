# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2021-08-14 13:28
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0025_account_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='purchase_sum',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Сумма всех покупок'),
        ),
    ]