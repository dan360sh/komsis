# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2021-08-13 09:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoggingEmail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('to', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=200)),
                ('ok', models.BooleanField(default=False)),
            ],
        ),
    ]
