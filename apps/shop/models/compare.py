from apps.account.models import Account
from apps.catalog.models import Product
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Compare(models.Model):
    """Модель сравнения товаров"""

    account = models.OneToOneField(
        Account, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.account.user.username

    def items(self):
        return self.compare_items.all()

    def count(self):
        return len(self.items())

    class Meta:
        verbose_name = "избранные товары"
        verbose_name_plural = "Избранные товары"


class CompareItem(models.Model):
    """Модель элементов избранных товаров"""

    compare = models.ForeignKey(
        Compare, related_name="compare_items", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="product_compare_items", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "элемент товаров для сравнения"
        verbose_name_plural = "Элементы товаров для сравнения"


@receiver(post_save, sender=Account)
def create_compare(sender, instance, created, **kwargs):
    """Создание новой модели избранных товаров пользователя личного кабинета.

    Модель избранных товаров создается по сигналу сохраненного пользователя
    личного кабинета, и привязывается к созданному пользователю. Модель
    избранных товаров создается только в том случае если пользователь был
    создан, а не просто сохранен.

    Arguments:
        sender {Account} -- Модель пользователя личного кабинета
        instance {Compare} -- Экземпляр пользователя личного кабинета
        created {bool} -- Показывает был ли создан профиль пользователя
    """

    if created:
        Compare.objects.create(account=instance)


@receiver(post_save, sender=Account)
def save_compare(sender, instance, **kwargs):
    """Сохранение модели уже существующей корзины пользователя личного кабинета.

    Корзина сохраняется по сигнялу сохранения пользователя личного кабинета.

    Arguments:
        sender {Account} -- Модель пользователя личного кабинета
        instance {Compare} -- Экземпляр пользователя личного кабинета
    """

    instance.compare.save()


class UnauthCompare:
    """Избранные товары неавторизованного пользователя"""

    def __init__(self, compare_items=list()):
        self.compare_items = compare_items

    def items(self):
        return self.compare_items

    def count(self):
        return len(self.compare_items)


class UnauthCompareItem:
    """Элемент избранных товаров неавторизованного пользователя."""

    def __init__(self, product=None):
        self.product = product
