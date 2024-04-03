from apps.catalog.models import Option, Product
from django.db import models

DEFAULT_PRICE = 'a6bfe5d1-ccce-11dd-8d29-001fc6b4b87e'


class PriceType(models.Model):
    id_1c = models.CharField(
        verbose_name="Идентификатор из 1с",
        max_length=200,
        primary_key=True
    )
    title = models.CharField(
        verbose_name="Наименование типа цены",
        max_length=200
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Тип цены'
        verbose_name_plural = 'Типы цен'

    @classmethod
    def get_by_title(cls, title: str):
        try:
            return cls.objects.get(title=title)
        except cls.DoesNotExist:
            return None


class ProductPrice(models.Model):

    # default = "Розница"
    type = models.ForeignKey(
        'PriceType', verbose_name="Тип цены",
        max_length=200,
        null=True, on_delete=models.SET_NULL,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар',
        related_name='prices'
    )
    value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Значение цены',
        default=0
    )
    old_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Старая цена',
        default=0
    )

    class Meta:
        verbose_name = "Цена товара"
        verbose_name_plural = "Цены товаров"
        unique_together = ('type', 'product')

    def __str__(self):
        return str(self.product)


class OptionPrice(models.Model):
    type = models.ForeignKey(PriceType, verbose_name="Тип цены",
                             related_name="options", null=True, on_delete=models.SET_NULL,)
    option = models.ForeignKey(Option, verbose_name="Характеристика",
                               related_name="prices", on_delete=models.CASCADE,)
    value = models.DecimalField(max_digits=10, decimal_places=2,
                                verbose_name="Значение цены", default=0)
    old_value = models.DecimalField(max_digits=10, decimal_places=2,
                                    verbose_name="Старое значение цены", default=0)

    class Meta:
        verbose_name = "Цена характеристики"
        verbose_name_plural = "Цены характеристик"
        unique_together = ("type", "option")

    def __str__(self):
        return str(self.option)


def get_default_price_type() -> str:
    """Возвращает дефолтное значение ИД типа цены, если такого нет - создает."""
    price_type = PriceType.objects.filter(
        id_1c=DEFAULT_PRICE
    )

    if price_type.exists():
        return price_type.first().id_1c

    price_type = PriceType.objects.create(
        id_1c=DEFAULT_PRICE,
        title="Розница"
    )
    return price_type.id_1c
