# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2021-12-23 19:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0010_settings_time_work_cherep'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='work_time_end',
            field=models.TimeField(null=True, verbose_name='Время окончания рабочего дня'),
        ),
        migrations.AddField(
            model_name='city',
            name='work_time_start',
            field=models.TimeField(null=True, verbose_name='Время начала рабочего дня'),
        ),
    ]
