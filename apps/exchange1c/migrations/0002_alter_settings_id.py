# Generated by Django 4.0.5 on 2022-07-13 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange1c', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
