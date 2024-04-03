# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2021-03-19 14:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0004_typeshipping_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='payment_text',
            field=models.TextField(blank=True, default='', verbose_name="Текст 'Оплата' в карточке товара"),
        ),
        migrations.AddField(
            model_name='settings',
            name='shipping_text',
            field=models.TextField(blank=True, default='', verbose_name="Текст 'Доставка' в карточке товара"),
        ),
    ]
