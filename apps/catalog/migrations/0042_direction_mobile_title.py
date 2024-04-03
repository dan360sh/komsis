# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2022-01-20 14:58
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0041_direction_mobile_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='direction',
            name='mobile_title',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Название для мобильных телефонов'),
        ),
    ]
