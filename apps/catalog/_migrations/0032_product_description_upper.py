# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2020-03-06 08:41
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0031_product_rent'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description_upper',
            field=ckeditor_uploader.fields.RichTextUploadingField(default=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Описание товара'), null=True, verbose_name='Описание UPPER'),
        ),
    ]