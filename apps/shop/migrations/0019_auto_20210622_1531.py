# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2021-06-22 12:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0018_auto_20210622_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='is_deleted',
            field=models.BooleanField(default=False, help_text='Вместо удаления заказа отметьте этот пункт', verbose_name='Заказ удален?'),
        ),
    ]
