# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2020-06-30 09:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='count_cherepovets',
            field=models.IntegerField(default=0, verbose_name='Количество в Череповце'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='count_vologda',
            field=models.IntegerField(default=0, verbose_name='Количество в Вологде'),
        ),
    ]
