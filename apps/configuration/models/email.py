from django.db import models
from .mixins import SortingMixin
from .cities import City


class ContactEmail(SortingMixin):
    city = models.ForeignKey(
        City, on_delete=models.CASCADE,
        related_name="email_objects",
        verbose_name="Город"
    )
    title = models.CharField(verbose_name="Заголовок", max_length=300)
    email = models.EmailField(verbose_name="Почта", max_length=300)
    show_city = models.BooleanField(default=False, verbose_name="Показывать город?")

    class Meta:
        verbose_name = "Почтовый адрес"
        verbose_name_plural = "Почтовые адреса"
