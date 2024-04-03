from django.db import models

from apps.configuration.models.mixins import SortingMixin
from .cities import City


class PhoneNumber(SortingMixin):
    city = models.ForeignKey(
        City, on_delete=models.CASCADE,
        related_name="phone_objects",
        verbose_name="Город"
    )
    title = models.CharField(verbose_name="Заголовок", max_length=300)
    phone = models.CharField(verbose_name="Телефон", max_length=300)

    class Meta:
        verbose_name = "Номер телефона"
        verbose_name_plural = "Номера телефона"
