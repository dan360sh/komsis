# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2020-06-04 09:54
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_export_date', models.DateTimeField(default=datetime.datetime.now, verbose_name='Дата последнего экспорта заказов')),
                ('process', models.BooleanField(verbose_name='Идет синхронизация')),
                ('import_title', models.CharField(max_length=300, verbose_name='название файла импорта')),
                ('offers_title', models.CharField(max_length=300, verbose_name='название файла цен')),
            ],
            options={
                'verbose_name': 'Настройки обмена',
                'verbose_name_plural': 'Настройки обмена',
            },
        ),
    ]
