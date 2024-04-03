# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2021-09-13 16:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations
import django.db.models.deletion
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
        ('configuration', '0006_typeshipping_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='slider',
            name='mobile_image',
            field=filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='slider_mobile_image', to=settings.FILER_IMAGE_MODEL, verbose_name='Изображение для мобильной версии'),
        ),
    ]