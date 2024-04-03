# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-12-26 06:21
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_auto_20190201_1602'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=300, verbose_name='Заголовок')),
                ('text', ckeditor_uploader.fields.RichTextUploadingField(default='', verbose_name='Текст')),
                ('sort', models.IntegerField(default=1, verbose_name='Сортировка')),
            ],
            options={
                'verbose_name': 'Вакансия',
                'verbose_name_plural': 'Вакансии',
            },
        ),
    ]
