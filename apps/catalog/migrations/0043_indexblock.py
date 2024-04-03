# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2022-02-28 09:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
        ('catalog', '0042_direction_mobile_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndexBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='Заголовок')),
                ('href', models.CharField(max_length=300, verbose_name='Ссылка')),
                ('is_active', models.BooleanField(default=True, verbose_name='Отображать блок?')),
                ('image', filer.fields.image.FilerImageField(on_delete=django.db.models.deletion.CASCADE, related_name='index_block_images', to=settings.FILER_IMAGE_MODEL, verbose_name='Картинка')),
            ],
            options={
                'verbose_name': 'Блок на главной странице',
                'verbose_name_plural': 'Блоки на главной странице',
            },
        ),
    ]
