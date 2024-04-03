# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-02-11 09:56
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion
import filer.fields.file


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0007_auto_20161016_1055'),
        ('catalog', '0015_auto_20190211_1205'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Подпись', max_length=300, verbose_name='Подпись')),
            ],
            options={
                'verbose_name': 'файл',
                'verbose_name_plural': 'файлы',
            },
        ),
        migrations.AddField(
            model_name='brand',
            name='slug',
            field=models.SlugField(max_length=300, null=True, unique=True, verbose_name='Слаг'),
        ),
        migrations.AddField(
            model_name='brand',
            name='text',
            field=ckeditor_uploader.fields.RichTextUploadingField(default='', verbose_name='Текст'),
        ),
        migrations.AddField(
            model_name='file',
            name='brand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='brand_files', to='catalog.Brand', verbose_name='Блок файлов'),
        ),
        migrations.AddField(
            model_name='file',
            name='obj',
            field=filer.fields.file.FilerFileField(on_delete=django.db.models.deletion.CASCADE, related_name='file_brand', to='filer.File', verbose_name='файл'),
        ),
    ]