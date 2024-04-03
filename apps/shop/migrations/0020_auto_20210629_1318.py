# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2021-06-29 10:18
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0019_auto_20210622_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='points_collected',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Количество баллов, которые пользователь получит после оплаты'),
        ),
        migrations.AlterField(
            model_name='order',
            name='points_spent',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Количество потраченных бонусов'),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_without_points',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Стоимость заказа без вычета бонусов'),
        ),
    ]