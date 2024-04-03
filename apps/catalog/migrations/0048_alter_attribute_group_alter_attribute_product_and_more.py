# Generated by Django 4.0.5 on 2022-06-01 13:46

import colorfield.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import filer.fields.image
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
        ('catalog', '0047_indexblock_sort'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attribute',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='attributes', to='catalog.attributesgroup', verbose_name='Группа'),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_attrbutes', to='catalog.product', verbose_name='Товар'),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='value',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='value_attrbutes', to='catalog.attributevalue', verbose_name='Значение'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='seo_img1',
            field=filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_seo_img1', to=settings.FILER_IMAGE_MODEL, verbose_name='SEO картинка 1'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='seo_img2',
            field=filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_seo_img2', to=settings.FILER_IMAGE_MODEL, verbose_name='SEO картинка 2'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='seo_img3',
            field=filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_seo_img3', to=settings.FILER_IMAGE_MODEL, verbose_name='SEO картинка 3'),
        ),
        migrations.AlterField(
            model_name='category',
            name='level',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='category',
            name='lft',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='category',
            name='rght',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='category',
            name='seo_img1',
            field=filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_seo_img1', to=settings.FILER_IMAGE_MODEL, verbose_name='SEO картинка 1'),
        ),
        migrations.AlterField(
            model_name='category',
            name='seo_img2',
            field=filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_seo_img2', to=settings.FILER_IMAGE_MODEL, verbose_name='SEO картинка 2'),
        ),
        migrations.AlterField(
            model_name='category',
            name='seo_img3',
            field=filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_seo_img3', to=settings.FILER_IMAGE_MODEL, verbose_name='SEO картинка 3'),
        ),
        migrations.AlterField(
            model_name='color',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='colors', to='catalog.product', verbose_name='Товар'),
        ),
        migrations.AlterField(
            model_name='color',
            name='value',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='colors', to='catalog.colorvalue', verbose_name='Значение'),
        ),
        migrations.AlterField(
            model_name='colorvalue',
            name='hex_color',
            field=colorfield.fields.ColorField(default='#000000', help_text='HEX color, as #RRGGBB', image_field=None, max_length=7, samples=None, verbose_name='Код'),
        ),
        migrations.AlterField(
            model_name='direction',
            name='mobile_thumbnail',
            field=filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='direction_thumbnail_mobile', to=settings.FILER_IMAGE_MODEL, verbose_name='Картинка для телефонов'),
        ),
        migrations.AlterField(
            model_name='numattribute',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='num_attributes', to='catalog.attributesgroup', verbose_name='Группа'),
        ),
        migrations.AlterField(
            model_name='numattribute',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_num_attrbutes', to='catalog.product', verbose_name='Товар'),
        ),
        migrations.AlterField(
            model_name='option',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='options', to='catalog.product', verbose_name='Товар'),
        ),
        migrations.AlterField(
            model_name='optionprice',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='options', to='catalog.pricetype', verbose_name='Тип цены'),
        ),
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='brand_products', to='catalog.brand', verbose_name='Производитель'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='catalog.category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='product',
            name='level',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='lft',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_child', to='catalog.product', verbose_name='Товар-родитель'),
        ),
        migrations.AlterField(
            model_name='product',
            name='rght',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='seo_img1',
            field=filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_seo_img1', to=settings.FILER_IMAGE_MODEL, verbose_name='SEO картинка 1'),
        ),
        migrations.AlterField(
            model_name='product',
            name='seo_img2',
            field=filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_seo_img2', to=settings.FILER_IMAGE_MODEL, verbose_name='SEO картинка 2'),
        ),
        migrations.AlterField(
            model_name='product',
            name='seo_img3',
            field=filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_seo_img3', to=settings.FILER_IMAGE_MODEL, verbose_name='SEO картинка 3'),
        ),
        migrations.AlterField(
            model_name='productgallery',
            name='photo',
            field=filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.FILER_IMAGE_MODEL, verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='productprice',
            name='type',
            field=models.ForeignKey(max_length=200, null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.pricetype', verbose_name='Тип цены'),
        ),
    ]
