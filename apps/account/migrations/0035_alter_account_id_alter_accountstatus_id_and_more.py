# Generated by Django 4.0.5 on 2022-07-13 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0034_alter_accountstatus_previous_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='accountstatus',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='discountcard',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='manager',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
