# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-09-04 06:35
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import filer.fields.file
import filer.fields.image


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('filer', '0007_auto_20161016_1055'),
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HrefModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_path', models.CharField(help_text='путь к объекту(модуль.класс.id)', max_length=500, unique=True, verbose_name='Путь к объекту')),
            ],
            options={
                'verbose_name_plural': 'ссылки на объект',
                'verbose_name': 'ссылка на объект',
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(choices=[('ru', 'Russian'), ('en', 'English')], max_length=32, unique=True, verbose_name='Язык')),
                ('name', models.CharField(blank=True, default='', max_length=300, verbose_name='Наименование сайта')),
                ('full_address', models.CharField(blank=True, default='', max_length=300, verbose_name='Полный адрес')),
                ('address', models.CharField(blank=True, default='', max_length=300, verbose_name='Адрес')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Email')),
                ('phones', models.CharField(blank=True, default='', help_text='разделитель ;', max_length=300, verbose_name='Номера телефонов')),
                ('time_work', models.CharField(blank=True, default='', max_length=300, verbose_name='Режим работы')),
                ('coord_x', models.FloatField(blank=True, null=True, verbose_name='Координата X на карте')),
                ('coord_y', models.FloatField(blank=True, null=True, verbose_name='Координата Y на карте')),
                ('privacy_policy', ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', verbose_name='Политика конфиденциальности')),
                ('personal_data', ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', verbose_name='Согласие на обработку персональных данных')),
                ('color_scheme', models.CharField(default='#007bff', max_length=7, verbose_name='Цветовая схема сайта')),
                ('vkontakte', models.CharField(blank=True, max_length=300, verbose_name='Ссылка на ВК группу')),
                ('facebook', models.CharField(blank=True, max_length=300, verbose_name='Ссылка на fb группу')),
                ('instagram', models.CharField(blank=True, max_length=300, verbose_name='Ссылка на instagram')),
                ('telegram', models.CharField(blank=True, max_length=300, verbose_name='Ссылка на telegram')),
                ('twitter', models.CharField(blank=True, max_length=300, verbose_name='Ссылка на twitter')),
                ('youtube', models.CharField(blank=True, max_length=300, verbose_name='Ссылка на youtube')),
                ('seo_text', ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', verbose_name='SEO текст')),
                ('meta_title', models.CharField(blank=True, default='', max_length=300, verbose_name='SEO Заголовок')),
                ('meta_description', models.TextField(blank=True, default='', verbose_name='Meta Description')),
                ('meta_template_description', models.TextField(blank=True, default='', verbose_name='Meta template Description')),
                ('meta_keywords', models.TextField(blank=True, default='', help_text='вводить через запятую', verbose_name='Meta Keywords')),
                ('meta_template_title', models.CharField(blank=True, default='', help_text=' ||site|| - имя сайта,\n        ||object|| - имя объекта ', max_length=300, verbose_name='Шаблон для сайта')),
                ('robots_txt', models.TextField(blank=True, default='', verbose_name='robots.txt')),
                ('head_scripts', models.TextField(blank=True, default='', verbose_name='Вывод в head')),
                ('scripts', models.TextField(blank=True, default='', verbose_name='Скрипты под footer')),
                ('mode_payment', models.CharField(choices=[('', 'Онлайн оплата отсутствует'), ('https://3dsec.sberbank.ru/payment/', 'Тестовый режим'), ('https://securepayments.sberbank.ru/payment/', 'Боевой режим')], default='', max_length=100, verbose_name='Режим оплаты')),
                ('shop_id', models.CharField(blank=True, default='', max_length=100, verbose_name='Режим оплаты')),
                ('api_key', models.CharField(blank=True, default='', max_length=100, verbose_name='Ключ api')),
                ('price_list', filer.fields.file.FilerFileField(blank=True, help_text='Узнайте о нас больше', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='catalog_company', to='filer.File', verbose_name='Прайс лист')),
                ('seo_img', filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='seo_img', to=settings.FILER_IMAGE_MODEL, verbose_name='SEO картинка')),
            ],
            options={
                'verbose_name_plural': 'Настройки сайта',
                'verbose_name': 'Настройки сайта',
                'ordering': ['language'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=100, verbose_name='Заголовок')),
                ('subtitle', models.CharField(blank=True, default='', max_length=300, verbose_name='Подзаголовок')),
                ('link', models.CharField(blank=True, default='', max_length=100, verbose_name='Ссылка')),
                ('image', filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='slider_image', to=settings.FILER_IMAGE_MODEL, verbose_name='Изображение')),
                ('settings', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slider_items', to='configuration.Settings', verbose_name='Настройки сайта')),
            ],
            options={
                'verbose_name_plural': 'Слайдер',
                'verbose_name': 'Элемент слайдера',
                'ordering': ['id'],
            },
        ),
    ]