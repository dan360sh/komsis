# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2021-08-16 13:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0030_account_clear_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountstatus',
            name='code',
            field=models.CharField(choices=[('000000002', 'LOYAL'), ('000000001', 'NEW'), ('000000003', 'VIP')], default='000000001', max_length=200, verbose_name='Код'),
        ),
    ]