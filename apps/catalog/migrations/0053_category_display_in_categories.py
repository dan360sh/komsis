# Generated by Django 4.0.6 on 2023-05-31 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0052_category_display_related_categories_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='display_in_categories',
            field=models.BooleanField(default=True, verbose_name='Отображать в списке категорий'),
        ),
    ]