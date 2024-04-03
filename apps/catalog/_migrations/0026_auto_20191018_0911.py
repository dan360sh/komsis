# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-10-18 06:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0025_auto_20191014_1653'),
    ]

    operations = [
        migrations.AddField(
            model_name='option',
            name='level',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='option',
            name='lft',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='option',
            name='rght',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='option',
            name='tree_id',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
            preserve_default=False,
        ),
    ]