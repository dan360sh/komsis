# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2021-05-27 11:16
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_auto_20210525_1941'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiscountCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Наименвоание скидочной карты')),
                ('percent', models.DecimalField(decimal_places=1, max_digits=4, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Процент скидки')),
                ('id_1c', models.CharField(max_length=200, verbose_name='ИД из 1с')),
            ],
        ),
    ]
