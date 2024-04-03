# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-10-28 15:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0014_auto_20181026_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='typeshipping',
            name='cities',
            field=models.TextField(blank=True, default='', help_text='разделитель ;', verbose_name='Доставляется только в ...(города)'),
        ),
        migrations.AlterField(
            model_name='typeshipping',
            name='cities_free',
            field=models.TextField(blank=True, default='', help_text='разделитель ;', verbose_name='Города с бесплатной доставкой'),
        ),
    ]
