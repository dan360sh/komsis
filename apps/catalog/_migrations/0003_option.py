# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-10-05 14:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_remove_attributesgroup_type_attr'),
    ]

    operations = [
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, null=True, verbose_name='Заголовок')),
                ('price', models.FloatField(default=0, null=True, verbose_name='Цена')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='options', to='catalog.Product', verbose_name='Товар')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'опция',
                'verbose_name_plural': 'Опции',
            },
        ),
    ]
