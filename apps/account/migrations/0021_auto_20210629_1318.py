# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2021-06-29 10:18
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0020_account_valid_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='points_total',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Количество баллов'),
        ),
        migrations.AlterField(
            model_name='account',
            name='unconfirmed_points',
            field=models.FloatField(default=0, help_text='\n            Эти баллы будут постепенно переходить на основной\n            бонусный счет пользователя,\n            по мере оплаты им его заказов\n            ', validators=[django.core.validators.MinValueValidator(0)], verbose_name='Неподтвержденные баллы'),
        ),
    ]