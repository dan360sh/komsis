# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-10-03 17:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attributesgroup',
            name='type_attr',
        ),
    ]
