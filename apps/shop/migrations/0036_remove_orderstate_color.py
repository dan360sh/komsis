# Generated by Django 4.0.6 on 2023-09-27 13:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0035_alter_cart_id_alter_cartitem_id_alter_compare_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderstate',
            name='color',
        ),
    ]