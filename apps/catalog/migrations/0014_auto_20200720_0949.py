# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2020-07-20 06:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0013_auto_20200717_1611'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(verbose_name='Стоимость')),
                ('option', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='catalog.Option', verbose_name='Вариативный товар')),
            ],
            options={
                'verbose_name': 'Цены по типу',
                'verbose_name_plural': 'Цены по типам',
                'ordering': ['price_type'],
            },
        ),
        migrations.CreateModel(
            name='ProductPriceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unloading_id', models.CharField(max_length=257, verbose_name='ID выгрузки')),
                ('title', models.CharField(max_length=55, unique=True, verbose_name='Название')),
                ('sort', models.PositiveSmallIntegerField(default=0, verbose_name='Сортировка')),
            ],
            options={
                'verbose_name': 'Тип цены',
                'verbose_name_plural': 'Типы цен',
                'ordering': ['sort'],
            },
        ),
        migrations.AddField(
            model_name='productprice',
            name='price_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.ProductPriceType', verbose_name='Тип цены'),
        ),
        migrations.AddField(
            model_name='productprice',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='catalog.Product', verbose_name='Продукт'),
        ),
        migrations.AlterUniqueTogether(
            name='productprice',
            unique_together=set([('price_type', 'option'), ('price_type', 'product')]),
        ),
    ]