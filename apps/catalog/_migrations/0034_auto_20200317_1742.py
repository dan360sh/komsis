# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2020-03-17 14:42
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0033_auto_20200306_1159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='text_upper',
            field=ckeditor_uploader.fields.RichTextUploadingField(db_index=True, default=ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', verbose_name='Текст'), null=True, verbose_name='Текст UPPER'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='title_upper',
            field=models.CharField(db_index=True, default=models.CharField(default='', max_length=300, verbose_name='Заголовок'), max_length=300, null=True, verbose_name='Заголовок UPPER'),
        ),
        migrations.AlterField(
            model_name='product',
            name='code',
            field=models.CharField(blank=True, db_index=True, max_length=300, verbose_name='Код товара'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description_upper',
            field=ckeditor_uploader.fields.RichTextUploadingField(db_index=True, default=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Описание товара'), null=True, verbose_name='Описание UPPER'),
        ),
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(max_length=300, null=True, verbose_name='Наименование'),
        ),
        migrations.AlterField(
            model_name='product',
            name='title_upper',
            field=models.CharField(db_index=True, default=models.CharField(max_length=300, null=True, verbose_name='Наименование'), max_length=300, null=True, verbose_name='Наименование UPPER'),
        ),
    ]
