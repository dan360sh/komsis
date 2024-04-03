from django.db import models
from django.utils.translation import gettext_lazy as _

from .settings import Settings


class City(models.Model):
    settings = models.ForeignKey(Settings, verbose_name="Настройки сайта",
                                 related_name="city_items", on_delete=models.CASCADE)
    title = models.CharField(verbose_name="Название", max_length=100,
                             default="", blank=True)
    address = models.CharField(verbose_name="Адрес", max_length=300,
                               default="", blank=True)
    phones = models.CharField(verbose_name="Номера телефонов",
                              help_text="разделитель ;", default="",
                              blank=True, max_length=300)
    email = models.EmailField(verbose_name="Email", blank=True, null=False)
    time_work = models.CharField(verbose_name="Режим работы", max_length=300,
                                 default="", blank=True)
    coord_x = models.FloatField(verbose_name="Координата X на карте",
                                blank=True, null=True)
    coord_y = models.FloatField(verbose_name="Координата Y на карте",
                                blank=True, null=True)
    work_time_start = models.TimeField(verbose_name="Время начала рабочего дня",
                                       null=True)
    work_time_end = models.TimeField(verbose_name="Время окончания рабочего дня",
                                     null=True)

    def __str__(self):
        return self.title

    def get_phones(self):
        return self.phone_objects.all().order_by("sort")

    def get_emails(self):
        return self.email_objects.all().order_by("sort")

    def get_vacancies(self):
        return self.vacancies.all().order_by("sort")

    class Meta:
        verbose_name = _('Город')
        verbose_name_plural = _('Города')
        ordering = ['id']
