# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2020-05-18 11:19
from __future__ import unicode_literals

import ckeditor_uploader.fields
import django.contrib.postgres.indexes
import django.contrib.postgres.search
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0036_brand_search_vector'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='content_search',
            field=django.contrib.postgres.search.SearchVectorField(null=True),
        ),
        migrations.AddIndex(
            model_name='product',
            index=django.contrib.postgres.indexes.GinIndex(fields=['content_search'], name='catalog_pro_content_b82ff0_gin'),
        ),
    ]
