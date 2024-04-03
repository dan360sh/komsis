# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-12-25 12:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collapser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=300, verbose_name='Заголовок')),
                ('text', models.TextField(default='', verbose_name='Текст')),
                ('sort', models.IntegerField(default=1, verbose_name='Сортировка')),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='content_collapser', to='content.Content')),
            ],
        ),
    ]