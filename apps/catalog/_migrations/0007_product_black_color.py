# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-02-01 07:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_product_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='black_color',
            field=models.BooleanField(default=False, help_text='Иначе белый', verbose_name='Черный текст в карточке на главной'),
        ),
    ]
