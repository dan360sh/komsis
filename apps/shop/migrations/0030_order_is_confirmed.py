# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2021-08-17 11:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0029_orderstate_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_confirmed',
            field=models.BooleanField(default=False, help_text="Техническое поле необходимое дляобновления поля 'сумма покупок'у пользовтеля, совершившего заказ", verbose_name='Заказ был подтевержден'),
        ),
    ]
