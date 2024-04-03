from django.db import models
from django.db.models import Sum
from django.core.validators import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver


class ProductStorage(models.Model):
    """Склады"""
    upload_title = models.CharField('Название в выгрузке', max_length=127, unique=True, default='')
    title = models.CharField('Название', max_length=127, default='')
    address = models.CharField('Адрес', max_length=127, default='', blank=True)
    city = models.ForeignKey('configuration.City', verbose_name="Город", on_delete=models.CASCADE,
                             blank=True, null=True)

    class Meta:
        ordering = ['city']
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

    def __str__(self):
        return self.title


class ProductStorageCount(models.Model):
    """Остатки на складе"""
    product = models.ForeignKey('catalog.Product', verbose_name='Продукт', on_delete=models.CASCADE,
                                related_name='storages', blank=True, null=True)
    option = models.ForeignKey('catalog.Option', verbose_name="Вариативный товар", on_delete=models.CASCADE,
                               related_name='storages', blank=True, null=True)
    storage = models.ForeignKey('catalog.ProductStorage', verbose_name='Склад', on_delete=models.CASCADE)
    count = models.FloatField('Количество')

    class Meta:
        ordering = ['product']
        verbose_name = 'Остатки на складе'
        verbose_name_plural = 'Остатки на складах'
        unique_together = (
            ('storage', 'product'),
            ('storage', 'option'),
        )

    def __str__(self):
        if self.product:
            title = self.product.__str__()
        else:
            title = self.option.__str__()
        return title + self.storage.__str__() + str(self.count)

    def full_clean(self, exclude=None, validate_unique=True):
        if bool(self.product) == bool(self.option):
            raise ValidationError("Нужно выбрать продукт или вариацию продукта", code='invalid')


@receiver(post_save, sender=ProductStorageCount)
def set_total_count_instance(instance, sender, created, **kwargs):
    """Устанавливает общее количество товаров"""
    item = instance.product if instance.product else instance.option
    item.count = item.get_total_count()
    item.save(update_fields=['count'])
