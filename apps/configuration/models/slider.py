from django.db import models
from django.db.models.fields import BLANK_CHOICE_DASH, related
from django.utils.translation import gettext_lazy as _
from filer.fields.image import FilerImageField

from ..models import Settings


class Slider(models.Model):
    settings = models.ForeignKey(Settings, verbose_name="Настройки сайта",
                                 related_name="slider_items", on_delete=models.CASCADE)
    image = FilerImageField(verbose_name="Изображение", blank=True, null=True,
                            related_name="slider_image",
                            on_delete=models.SET_NULL)
    mobile_image = FilerImageField(verbose_name="Изображение для мобильной версии",
                                   related_name="slider_mobile_image",
                                   blank=True, null=True,
                                   on_delete=models.SET_NULL)
    title = models.CharField(verbose_name="Заголовок",
                             blank=True, default="", max_length=100)
    subtitle = models.CharField(verbose_name="Подзаголовок",
                                blank=True, default="", max_length=300)
    link = models.CharField(verbose_name="Ссылка",
                            blank=True, default="", max_length=10000)
    sort = models.PositiveIntegerField(verbose_name="Сортировка", default=500)

    def __str__(self):
        return 'Элемент слайдера №' + str(self.id)

    class Meta:
        verbose_name = _('Элемент слайдера')
        verbose_name_plural = _('Слайдер')
        ordering = ['sort']
