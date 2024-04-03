# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-09-04 06:35
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.Account')),
            ],
            options={
                'verbose_name_plural': 'Корзины',
                'verbose_name': 'корзина',
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0, verbose_name='Количество')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='shop.Cart')),
                ('color', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.Color', verbose_name='Цвет')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Product', verbose_name='Товар')),
            ],
            options={
                'verbose_name_plural': 'элементы корзины',
                'verbose_name': 'элемент корзины',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Compare',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.Account')),
            ],
            options={
                'verbose_name_plural': 'Избранные товары',
                'verbose_name': 'избранные товары',
            },
        ),
        migrations.CreateModel(
            name='CompareItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('compare', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='compare_items', to='shop.Compare')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_compare_items', to='catalog.Product')),
            ],
            options={
                'verbose_name_plural': 'Элементы товаров для сравнения',
                'verbose_name': 'элемент товаров для сравнения',
            },
        ),
        migrations.CreateModel(
            name='Favorites',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.Account')),
            ],
            options={
                'verbose_name_plural': 'Избранные товары',
                'verbose_name': 'избранные товары',
            },
        ),
        migrations.CreateModel(
            name='FavoritesItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('waiting', models.BooleanField(default=False, verbose_name='Ожидание')),
                ('favorites', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites_items', to='shop.Favorites')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_fovorites_items', to='catalog.Product')),
            ],
            options={
                'verbose_name_plural': 'Эементы избранных товаров',
                'verbose_name': 'элемент избранных товаров',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=300, verbose_name='Имя')),
                ('phone', models.CharField(default='', max_length=300, verbose_name='Телефон')),
                ('email', models.EmailField(default='', max_length=254, verbose_name='Email')),
                ('date', models.DateTimeField(default=datetime.datetime.now, verbose_name='Дата заказа')),
                ('total', models.FloatField(blank=True, null=True, verbose_name='Общая стоимость заказа')),
                ('bank_id', models.CharField(blank=True, default='', max_length=100, verbose_name='Ид заказа в системе банка')),
                ('payment', models.BooleanField(default=False, verbose_name='Заказ оплачен')),
                ('status', models.CharField(choices=[('processing', 'В обработке'), ('completed', 'Выполнен'), ('canceled', 'Отменен')], default='processing', max_length=50, verbose_name='Статус')),
                ('type_payment', models.CharField(choices=[('bank', 'Банковской картой онлайн'), ('bill', 'Оплата по счету'), ('receiving', 'Оплата при получении')], default='receiving', max_length=50, verbose_name='Способ оплаты')),
                ('shipping', models.CharField(choices=[('self', 'Самовывоз'), ('transport', 'Транспотной компанией'), ('post', 'Почтой'), ('courier', 'Курьером')], default='self', max_length=50, verbose_name='Доставка')),
                ('post_code', models.PositiveIntegerField(blank=True, null=True, verbose_name='Почтовый индекс')),
                ('region', models.CharField(blank=True, default='', max_length=200, verbose_name='Область')),
                ('district', models.CharField(blank=True, default='', max_length=200, verbose_name='Район')),
                ('city', models.CharField(blank=True, default='', max_length=200, verbose_name='Нас. пункт')),
                ('street', models.CharField(blank=True, default='', max_length=200, verbose_name='Улица')),
                ('house', models.CharField(blank=True, default='', max_length=200, verbose_name='Дом')),
                ('housing', models.CharField(blank=True, default='', max_length=100, verbose_name='Корпус')),
                ('apartment', models.CharField(blank=True, default='', max_length=50, verbose_name='Квартира')),
                ('comment', models.TextField(blank=True, default='', verbose_name='Комментарий')),
                ('account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='account.Account', verbose_name='Профиль')),
            ],
            options={
                'verbose_name_plural': 'Заказы',
                'verbose_name': 'заказ',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0, verbose_name='Количество')),
                ('total', models.FloatField(blank=True, default=0, verbose_name='Цена на момент покупки')),
                ('color', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='color_order_items', to='catalog.Color', verbose_name='Опция')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='shop.Order', verbose_name='Заказ')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_order_items', to='catalog.Product', verbose_name='Товар')),
            ],
            options={
                'verbose_name_plural': 'Элементы заказа',
                'verbose_name': 'элемент заказа',
            },
        ),
    ]
