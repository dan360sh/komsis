from apps.account.models import Account
from apps.catalog.models import Product
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Favorites(models.Model):
    """Модель избарнных товаров"""

    account = models.OneToOneField(
        Account, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.account.user.username

    def items(self):
        return self.favorites_items.all()

    def count(self):
        return len(self.items())

    class Meta:
        verbose_name = "избранные товары"
        verbose_name_plural = "Избранные товары"


class FavoritesItem(models.Model):
    """Модель элементов избранных товаров"""

    favorites = models.ForeignKey(
        Favorites, related_name="favorites_items", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="product_fovorites_items", on_delete=models.CASCADE)
    waiting = models.BooleanField(verbose_name="Ожидание", default=False)

    class Meta:
        verbose_name = "элемент избранных товаров"
        verbose_name_plural = "Эементы избранных товаров"


@receiver(post_save, sender=Account)
def create_favorites(sender, instance, created, **kwargs):
    """Создание новой модели избранных товаров пользователя личного кабинета.

    Модель избранных товаров создается по сигналу сохраненного пользователя
    личного кабинета, и привязывается к созданному пользователю. Модель
    избранных товаров создается только в том случае если пользователь был
    создан, а не просто сохранен.

    Arguments:
        sender {Account} -- Модель пользователя личного кабинета
        instance {Favorites} -- Экземпляр пользователя личного кабинета
        created {bool} -- Показывает был ли создан профиль пользователя
    """

    if created:
        Favorites.objects.create(account=instance)


@receiver(post_save, sender=Account)
def save_favorites(sender, instance, **kwargs):
    """Сохранение модели уже существующей корзины пользователя личного кабинета.

    Корзина сохраняется по сигнялу сохранения пользователя личного кабинета.

    Arguments:
        sender {Account} -- Модель пользователя личного кабинета
        instance {Favorites} -- Экземпляр пользователя личного кабинета
    """

    instance.favorites.save()


class UnauthFavorites:
    """Избранные товары неавторизованного пользователя"""

    def __init__(self, favorites_items=list()):
        self.favorites_items = favorites_items

    def items(self):
        return self.favorites_items

    def count(self):
        return len(self.favorites_items)


class UnauthFavoritesItem:
    """Элемент избранных товаров неавторизованного пользователя."""

    def __init__(self, product=None):
        self.product = product
