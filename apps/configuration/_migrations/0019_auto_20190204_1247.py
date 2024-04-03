# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-02-04 09:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0018_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='coord_x',
            field=models.FloatField(blank=True, null=True, verbose_name='Координата X на карте'),
        ),
        migrations.AddField(
            model_name='city',
            name='coord_y',
            field=models.FloatField(blank=True, null=True, verbose_name='Координата Y на карте'),
        ),
    ]