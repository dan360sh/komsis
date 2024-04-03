# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2021-08-31 08:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations
import django.db.models.deletion
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='galleryitem',
            name='backing_image',
            field=filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gallery_backing_images', to=settings.FILER_IMAGE_MODEL, verbose_name='Дополнительное изображение'),
        ),
    ]
