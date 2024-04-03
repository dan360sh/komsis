import re

from apps.account.models import Account
from apps.catalog.models import DEFAULT_PRICE, Color, Option, Product
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Cart(models.Model):
    """Модель корзины пользователя личного кабинета"""

    account = models.OneToOneField(
        Account, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.account.user.username

    def count(self):
        return self.items().count()

    def items(self):
        return self.cart_items.all()

    def total(self):
        total = float()
        for item in self.items():
            total += float(item.total())
        # 24.04.2020 15:10
        # return total
        return round(total, 2)

    def count_total_by_account(self, account):
        total = float()
        for item in self.items():
            total += float(item.count_total_by_account(account))

        return round(total, 2)

    def clear(self):
        self.cart_items.all().delete()

    def register_item(self, item):
        product = Product.objects.get(id=item.product.id)
        option = item.option
        fields = {'count': item.count}
        cart_item, created = CartItem.objects.select_related('product').get_or_create(
            cart=self, product=product,
            defaults=fields, option=option
        )

    @property
    def has_overflow_items(self):
        for item in self.cart_items.all():
            if item.is_count_overflowed:
                return True
        return False

    @property
    def is_empty(self):
        return self.items().count() < 1

    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'Корзины'


class CartItem(models.Model):
    """Модель элемента корзины пользователя личного кабинета"""

    cart = models.ForeignKey(
        Cart, related_name="cart_items", on_delete=models.CASCADE)

    product = models.ForeignKey(
        Product, verbose_name="Товар", on_delete=models.CASCADE,)
    # product_id = models.IntegerField(verbose_name='id продукта', default=0)

    color = models.ForeignKey(Color, verbose_name="Цвет",
                              blank=True, null=True, on_delete=models.SET_NULL)

    option = models.ForeignKey(
        Option, verbose_name="Опция", blank=True, null=True, on_delete=models.SET_NULL)
    # option_id = models.IntegerField(verbose_name='id опции', blank=True, null=True)

    count = models.IntegerField(verbose_name="Количество", default=0)

    def price(self):
        if self.color:
            return self.color.price
        if self.option:
            return self.option.price
        return self.product.price

    def count_price_by_account(self, account):
        # if account.is_price_type_default and not self.option:
        #     return self.price()

        if self.option:
            return self.option.get_price_by_account(account)

        price = self.product.get_price_by_account(account)
        return price

    def total(self):
        if self.color:
            return self.color.price * self.count
        if self.option:
            return self.option.price * self.count
        return self.product.price * self.count

    def count_total_by_account(self, account):
        # if account.is_price_type_default:
        #     return self.total()

        if self.option:
            return self.option.get_price_by_account(account) * self.count

        price = self.product.get_price_by_account(account)
        return round(price * self.count, 2)

    @property
    def is_count_overflowed(self):
        if self.option:
            return self.count > self.option.get_total_count()
        return self.count > self.product.get_total_count()

    """# свойство продукта
    def get_product(self):
        return Product.objects.get(id=self.product_id)

    def set_product(self, product):
        self.product_id = product.id

    def del_product(self):
        self.product_id = None

    product = property(get_product, set_product, del_product, 'Продукт')

    # свойство опции
    def get_option(self):
        return Option.objects.get(id=self.option_id)

    def set_option(self, option):
        self.option_id = option.id

    def del_option(self):
        self.option_id = None

    option = property(get_option, set_option, del_option, 'Опция')"""

    class Meta:
        verbose_name = 'элемент корзины'
        verbose_name_plural = 'элементы корзины'
        ordering = ['id']


@receiver(post_save, sender=Account)
def create_cart(sender, instance, created, **kwargs):
    """Создание новой модели корзины пользователя личного кабинета.

    Корзина создается по сигналу сохраненного пользователя личного кабинета,
    и привязывается к созданному пользователю личного кабинета. Корзина
    создается только в том случае если профиль был создан, а не просто
    сохранен.

    Arguments:
        sender {Account} -- Модель пользователя личного кабинета
        instance {Cart} -- Экземпляр пользователя личного кабинета
        created {bool} -- Показывает был ли создан профиль пользователя
    """

    if created:
        Cart.objects.create(account=instance)


@receiver(post_save, sender=Account)
def save_cart(sender, instance, **kwargs):
    """Сохранение модели уже существующей корзины пользователя личного кабинета.

    Корзина сохраняется по сигнялу сохранения пользователя личного кабинета.

    Arguments:
        sender {Account} -- Модель пользователя личного кабинета
        instance {Cart} -- Экземпляр пользователя личного кабинета
    """

    instance.cart.save()


class UnauthCart:
    """Корзина неавторизованного пользователя"""

    _cart_items = []

    def __init__(self, cart_items=list()):
        self._cart_items = cart_items

    def items(self):
        res = []
        for item in self._cart_items:
            if item.product:
                if item.product.options.count() <= 0:
                    res.append(item)
                elif item.option:
                    res.append(item)
        return res

    def add(self, item):
        self._cart_items.append(item)

    # cart_items property
    def get_cart_items(self):
        return self.items()

    def set_cart_items(self, items):
        self._cart_items = items

    def del_cart_items(self):
        self._cart_items = []

    cart_items = property(get_cart_items, set_cart_items,
                          del_cart_items, 'Товары корзины')

    def count(self):
        return len(self.items())

    def total(self):
        total = float()
        cart_items = self.items()
        for item in cart_items:
            total += float(item.total())
        return total

    def count_total_by_account(self, account):
        total = float()
        cart_items = self.items()
        for item in cart_items:
            total += float(item.count_total_by_account(account))
        return total

    @property
    def has_overflow_items(self):
        for item in self.items():
            if item.is_count_overflowed:
                return True
        return False

    @property
    def is_empty(self):
        return self.count() < 1


class UnauthCartItem:
    """Элемент корзины неавторизованного пользователя."""

    product_id = None
    option_id = None
    color_id = None

    # свойство продукта
    def get_product(self):
        try:
            return Product.objects.get(id=self.product_id)
        except:
            return None

    def set_product(self, product):
        if product:
            self.product_id = product.id
        else:
            self.product_id = None

    def del_product(self):
        self.product_id = None

    product = property(get_product, set_product, del_product, 'Продукт')

    # свойство опции
    def get_option(self):
        try:
            return Option.objects.get(id=self.option_id)
        except:
            return None

    def set_option(self, option):
        if option:
            self.option_id = option.id
        else:
            self.option_id = None

    def del_option(self):
        self.option_id = None

    option = property(get_option, set_option, del_option, 'Опция')

    # свойство цвета
    def get_color(self):
        try:
            return Color.objects.get(id=self.color_id)
        except:
            return None

    def set_color(self, color):
        if color:
            self.color_id = color.id
        else:
            self.color_id = None

    def del_color(self):
        self.color_id = None

    color = property(get_color, set_color, del_color, 'Цвет')

    def __init__(self, product=None, color=None, count=None, option=None):
        self.product = product
        self.color = color
        self.count = count
        self.option = option

    def price(self):
        if self.color:
            return self.color.price
        if self.option:
            return self.option.price
        return self.product.price

    def total(self):
        if self.color:
            return self.color.price * self.count
        if self.option:
            return self.option.price * self.count
        return self.product.price * self.count

    def count_price_by_account(self, account):
        # if account.is_price_type_default:
        #     return self.price()

        price = self.product.get_price_by_account(account)
        return price

    def count_total_by_account(self, account):
        # if account.is_price_type_default:
        #     return self.total()

        return self.product.get_price_by_account(account) * self.count

    @property
    def is_count_overflowed(self):
        if self.option:
            return self.count > self.option.get_total_count()
        return self.count > self.product.get_total_count()
