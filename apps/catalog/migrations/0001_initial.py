# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2020-06-04 09:54
from __future__ import unicode_literals

import ckeditor_uploader.fields
import colorfield.fields
from django.conf import settings
import django.contrib.postgres.indexes
from django.db import migrations, models
import django.db.models.deletion
import filer.fields.file
import filer.fields.image
import mptt.fields
from django.contrib.postgres.operations import BtreeGinExtension

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('filer', '0007_auto_20161016_1055'),
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
    ]

    operations = [
        BtreeGinExtension(),
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unloading_id', models.CharField(blank=True, default='', max_length=300, verbose_name='Идентификатор выгрузки')),
                ('sort', models.IntegerField(default=1, verbose_name='Сортировка')),
                ('name', models.CharField(blank=True, default='', max_length=300, verbose_name='Сериализованное значение')),
            ],
            options={
                'verbose_name': 'атрибут',
                'verbose_name_plural': 'Атрибуты',
                'ordering': ['product', 'sort'],
            },
        ),
        migrations.CreateModel(
            name='AttributesGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unloading_id', models.CharField(blank=True, default='', max_length=300, verbose_name='Идентификатор выгрузки')),
                ('title', models.CharField(max_length=300, null=True, verbose_name='Заголовок')),
                ('type_value', models.IntegerField(choices=[(0, 'Справочник'), (1, 'Число')], default=0, verbose_name='Тип атрибута')),
                ('show', models.BooleanField(default=True, verbose_name='Показывать в категориях')),
            ],
            options={
                'verbose_name': 'группа атрибутов',
                'verbose_name_plural': 'Группы атрибутов',
            },
        ),
        migrations.CreateModel(
            name='AttributeValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unloading_id', models.CharField(blank=True, default='', max_length=300, verbose_name='Идентификатор выгрузки')),
                ('title', models.TextField(null=True, verbose_name='Заголовок')),
            ],
            options={
                'verbose_name': 'Значение атрибута',
                'verbose_name_plural': 'Значения атрибутов',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, verbose_name='Активность')),
                ('title', models.CharField(default='', max_length=300, verbose_name='Заголовок')),
                ('title_upper', models.CharField(db_index=True, default=models.CharField(default='', max_length=300, verbose_name='Заголовок'), max_length=300, null=True, verbose_name='Заголовок UPPER')),
                ('slug', models.SlugField(max_length=300, null=True, unique=True, verbose_name='Слаг')),
                ('text', ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', verbose_name='Текст')),
                ('text_upper', ckeditor_uploader.fields.RichTextUploadingField(default=ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', verbose_name='Текст'), null=True, verbose_name='Текст UPPER')),
                ('link', models.CharField(blank=True, default='', max_length=127, verbose_name='Ссылка')),
                ('sort', models.PositiveIntegerField(default=500, verbose_name='Сортировка')),
                ('thumbnail', filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='brand_thumbnail', to=settings.FILER_IMAGE_MODEL, verbose_name='Картинка')),
            ],
            options={
                'verbose_name': 'производитель',
                'verbose_name_plural': 'Производители',
                'ordering': ('sort',),
            },
        ),
        migrations.CreateModel(
            name='BrandFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Подпись', max_length=300, verbose_name='Подпись')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='brand_files', to='catalog.Brand', verbose_name='Блок файлов')),
                ('obj', filer.fields.file.FilerFileField(on_delete=django.db.models.deletion.CASCADE, related_name='file_brand', to='filer.File', verbose_name='файл')),
            ],
            options={
                'verbose_name': 'файл',
                'verbose_name_plural': 'файлы',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seo_text', ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', verbose_name='SEO текст')),
                ('meta_title', models.CharField(blank=True, default='', max_length=300, verbose_name='SEO заголовок')),
                ('meta_description', models.TextField(blank=True, null=True, verbose_name='Meta Description')),
                ('meta_keywords', models.TextField(blank=True, null=True, verbose_name='Meta Keywords')),
                ('active', models.BooleanField(default=True, verbose_name='Активность')),
                ('unloading_id', models.CharField(blank=True, default='', max_length=300, verbose_name='Идентификатор выгрузки')),
                ('title', models.CharField(db_index=True, max_length=300, null=True, verbose_name='Наименование')),
                ('slug', models.SlugField(max_length=300, null=True, unique=True, verbose_name='Слаг')),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', verbose_name='Описание')),
                ('black_color', models.BooleanField(default=False, help_text='Иначе белый', verbose_name='Черный текст в карточке на главной')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='childs', to='catalog.Category', verbose_name='Родитель')),
                ('seo_img1', filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='catalog_category_seo_img1', to=settings.FILER_IMAGE_MODEL, verbose_name='SEO картинка 1')),
                ('seo_img2', filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='catalog_category_seo_img2', to=settings.FILER_IMAGE_MODEL, verbose_name='SEO картинка 2')),
                ('seo_img3', filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='catalog_category_seo_img3', to=settings.FILER_IMAGE_MODEL, verbose_name='SEO картинка 3')),
                ('thumbnail', filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category_thumbnail', to=settings.FILER_IMAGE_MODEL, verbose_name='Миниатюра')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default=0, null=True, verbose_name='Цена')),
            ],
            options={
                'verbose_name': 'цвет',
                'verbose_name_plural': 'Цвета',
            },
        ),
        migrations.CreateModel(
            name='ColorValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, null=True, verbose_name='Заголовок')),
                ('hex_color', colorfield.fields.ColorField(default='#000000', help_text='HEX color, as #RRGGBB', max_length=18, verbose_name='Код')),
            ],
            options={
                'verbose_name': 'значение цвета',
                'verbose_name_plural': 'Значения цветов',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=300, verbose_name='Заголовок')),
            ],
            options={
                'verbose_name': 'страна',
                'verbose_name_plural': 'Страны',
            },
        ),
        migrations.CreateModel(
            name='Direction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=300, null=True, verbose_name='Наименование')),
                ('title_original', models.CharField(blank=True, default='', max_length=300, verbose_name='Оригинальное название')),
                ('black_color', models.BooleanField(default=False, help_text='Иначе белый', verbose_name='Черный текст в карточке на главной')),
                ('sort', models.PositiveIntegerField(default=500, verbose_name='Сортировка')),
                ('thumbnail', filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='direction_thumbnail', to=settings.FILER_IMAGE_MODEL, verbose_name='Картинка')),
            ],
            options={
                'verbose_name': 'Направление',
                'verbose_name_plural': 'Направления',
                'ordering': ['sort'],
            },
        ),
        migrations.CreateModel(
            name='NumAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unloading_id', models.CharField(blank=True, default='', max_length=300, verbose_name='Идентификатор выгрузки')),
                ('sort', models.IntegerField(default=1, verbose_name='Сортировка')),
                ('value', models.FloatField(verbose_name='Значение атрибута')),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='num_attributes', to='catalog.AttributesGroup', verbose_name='Группа')),
            ],
            options={
                'verbose_name': 'Числовой атрибут',
                'verbose_name_plural': 'Числовые атрибуты',
                'ordering': ['product', 'sort'],
            },
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unloading_id', models.CharField(max_length=50, unique=True, verbose_name='Ид 1С')),
                ('active', models.BooleanField(default=True, verbose_name='Активность')),
                ('title', models.CharField(max_length=300, null=True, verbose_name='Заголовок')),
                ('step', models.FloatField(default=1, verbose_name='Шаг')),
                ('count', models.FloatField(blank=True, default=0, verbose_name='Количество')),
                ('price', models.FloatField(default=0, null=True, verbose_name='Цена')),
            ],
            options={
                'verbose_name': 'опция',
                'verbose_name_plural': 'Опции',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seo_text', ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', verbose_name='SEO текст')),
                ('meta_title', models.CharField(blank=True, default='', max_length=300, verbose_name='SEO заголовок')),
                ('meta_description', models.TextField(blank=True, null=True, verbose_name='Meta Description')),
                ('meta_keywords', models.TextField(blank=True, null=True, verbose_name='Meta Keywords')),
                ('title', models.CharField(max_length=3000, null=True, verbose_name='Наименование')),
                ('title_upper', models.CharField(db_index=True, default=models.CharField(max_length=3000, null=True, verbose_name='Наименование'), max_length=3000, null=True, verbose_name='Наименование UPPER')),
                ('active', models.BooleanField(default=True, verbose_name='Активность')),
                ('unloading_id', models.CharField(blank=True, default='', max_length=300, verbose_name='Идентификатор выгрузки')),
                ('slug', models.SlugField(blank=True, null=True, unique=True, verbose_name='Слаг')),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Описание товара')),
                ('description_upper', ckeditor_uploader.fields.RichTextUploadingField(db_index=True, default=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Описание товара'), null=True, verbose_name='Описание UPPER')),
                ('code', models.CharField(blank=True, db_index=True, max_length=300, verbose_name='Код товара')),
                ('status', models.IntegerField(choices=[(1, 'В наличии'), (2, 'Ожидается поступление'), (3, 'Нет в наличии')], default=1, verbose_name='Статус')),
                ('price', models.FloatField(default=0, verbose_name='Цена')),
                ('old_price', models.FloatField(default=0, verbose_name='Старая цена')),
                ('wholesale_price', models.FloatField(default=0, verbose_name='Оптовая цена')),
                ('count', models.FloatField(blank=True, default=0, verbose_name='Количество')),
                ('unit', models.CharField(blank=True, default='', max_length=100, verbose_name='Единица измерения')),
                ('step', models.FloatField(default=1, verbose_name='Шаг')),
                ('new', models.BooleanField(default=False, verbose_name='Новинка')),
                ('hit', models.BooleanField(default=False, verbose_name='Хит')),
                ('sale', models.BooleanField(default=False, verbose_name='Распродажа')),
                ('units', models.CharField(blank=True, default='', max_length=100, verbose_name='Единицы измерения')),
                ('count_showing', models.IntegerField(default=0, verbose_name='Количество просмотров')),
                ('rent', models.BooleanField(default=False, verbose_name='Доступна аренда')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='brand_products', to='catalog.Brand', verbose_name='Производитель')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='catalog.Category', verbose_name='Категория')),
                ('directions', models.ManyToManyField(blank=True, related_name='direction_products', to='catalog.Direction', verbose_name='Направления')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_child', to='catalog.Product', verbose_name='Товар-родитель')),
                ('seo_img1', filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='catalog_product_seo_img1', to=settings.FILER_IMAGE_MODEL, verbose_name='SEO картинка 1')),
                ('seo_img2', filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='catalog_product_seo_img2', to=settings.FILER_IMAGE_MODEL, verbose_name='SEO картинка 2')),
                ('seo_img3', filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='catalog_product_seo_img3', to=settings.FILER_IMAGE_MODEL, verbose_name='SEO картинка 3')),
                ('thumbnail', filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_thumbnail', to=settings.FILER_IMAGE_MODEL, verbose_name='Фотография')),
            ],
            options={
                'verbose_name': 'товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.CreateModel(
            name='ProductGallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField(default=1, verbose_name='Позиция')),
                ('photo', filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.FILER_IMAGE_MODEL, verbose_name='Изображение')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_gallery', to='catalog.Product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'изображение',
                'verbose_name_plural': 'Галерея',
                'ordering': ['position'],
            },
        ),
        migrations.AddField(
            model_name='option',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='options', to='catalog.Product', verbose_name='Товар'),
        ),
        migrations.AddField(
            model_name='numattribute',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_num_attrbutes', to='catalog.Product', verbose_name='Товар'),
        ),
        migrations.AddField(
            model_name='color',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='colors', to='catalog.Product', verbose_name='Товар'),
        ),
        migrations.AddField(
            model_name='color',
            name='value',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='colors', to='catalog.ColorValue', verbose_name='Значение'),
        ),
        migrations.AddField(
            model_name='attribute',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attributes', to='catalog.AttributesGroup', verbose_name='Группа'),
        ),
        migrations.AddField(
            model_name='attribute',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_attrbutes', to='catalog.Product', verbose_name='Товар'),
        ),
        migrations.AddField(
            model_name='attribute',
            name='value',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='value_attrbutes', to='catalog.AttributeValue', verbose_name='Значение'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=django.contrib.postgres.indexes.GinIndex(fields=['title_upper', 'description_upper', 'code'], name='catalog_pro_title_u_aff2bb_gin'),
        ),
        migrations.AddIndex(
            model_name='category',
            index=django.contrib.postgres.indexes.GinIndex(fields=['title'], name='catalog_cat_title_a636fb_gin'),
        ),
        migrations.AddIndex(
            model_name='brand',
            index=django.contrib.postgres.indexes.GinIndex(fields=['title_upper'], name='catalog_bra_title_u_7977b4_gin'),
        ),
    ]
