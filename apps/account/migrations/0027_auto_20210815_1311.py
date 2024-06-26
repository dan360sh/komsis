# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2021-08-15 10:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0026_account_purchase_sum'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='accountstatus',
            options={'verbose_name': 'Статус аккаунта', 'verbose_name_plural': 'Статусы акканута'},
        ),
        migrations.AlterField(
            model_name='accountstatus',
            name='max_limit',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Максимальный порог'),
        ),
    ]
