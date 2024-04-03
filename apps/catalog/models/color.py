from colorfield.fields import ColorField
from django.db import models

from ..models import Product

# class ColorGroup(models.Model):
#     title = models.CharField(verbose_name="Заголовок",
#                              default="", max_length=300)
#     hex_color = models.CharField(
#         verbose_name="Цвет", default="#000000", max_length=7)

#     def __str__(self):
#         return self.title

#     class Meta:
#         verbose_name = "группа цветов"
#         verbose_name_plural = "Группы цветов"


class ColorValue(models.Model):
    title = models.CharField(verbose_name="Заголовок",
                             blank=False, null=True, max_length=300)
    # group = models.ForeignKey(ColorGroup, verbose_name="Группа",
    #                           null=True, related_name="color_values")
    hex_color = ColorField(
        default='#000000', verbose_name="Код", max_length=7,
        help_text=(u'HEX color, as #RRGGBB'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "значение цвета"
        verbose_name_plural = "Значения цветов"


class Color(models.Model):
    product = models.ForeignKey(Product, verbose_name="Товар", blank=False,
                                null=True, related_name="colors", on_delete=models.SET_NULL)
    value = models.ForeignKey(ColorValue, verbose_name="Значение", on_delete=models.SET_NULL,
                              null=True, related_name="colors")
    price = models.FloatField(
        verbose_name="Цена", blank=False, default=0, null=True)

    def __str__(self):
        return self.product.title + " - " + self.value.title

    class Meta:
        verbose_name = "цвет"
        verbose_name_plural = "Цвета"
