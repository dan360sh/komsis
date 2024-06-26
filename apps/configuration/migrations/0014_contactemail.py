# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2022-01-18 14:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0013_phonenumber_sort'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactEmail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort', models.IntegerField(default=1, verbose_name='Сортировка')),
                ('title', models.CharField(max_length=300, verbose_name='Заголовок')),
                ('email', models.EmailField(max_length=300, verbose_name='Почта')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='email_objects', to='configuration.City', verbose_name='Город')),
            ],
            options={
                'verbose_name': 'Почтовый адрес',
                'verbose_name_plural': 'Почтовые адреса',
            },
        ),
    ]
