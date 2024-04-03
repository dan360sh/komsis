# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2021-09-02 13:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_vacancy_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vacancies', to='configuration.City', verbose_name='Город'),
        ),
    ]
