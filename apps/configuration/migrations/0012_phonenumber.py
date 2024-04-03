# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2022-01-18 14:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0011_auto_20211223_2220'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='Заголовок')),
                ('phone', models.CharField(max_length=300, verbose_name='Телефон')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phone_objects', to='configuration.City', verbose_name='Город')),
            ],
            options={
                'verbose_name': 'Номер телефона',
                'verbose_name_plural': 'Номера телефона',
            },
        ),
    ]
