from django.db import models
from django.utils.functional import cached_property
from mptt.models import MPTTModel, TreeForeignKey

from apps.configuration.utils import HrefModel


class Navigation(MPTTModel):
    title = models.CharField(verbose_name="Заголовок", default="",
                             max_length=300)
    alias = models.CharField(verbose_name="Псевдоним", default="", blank=True,
                             max_length=120,
                             help_text="*нужен для поиска меню")
    parent = TreeForeignKey('self', verbose_name="Родитель",
                            related_name='child', blank=True, null=True,
                            on_delete=models.CASCADE)
    href = models.CharField(verbose_name="Ссылка", null=False, default="",
                            blank=True, max_length=300)
    object_href = models.ForeignKey(HrefModel, verbose_name="Ссылка на объект",
                                    null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title

    @cached_property
    def get_url(self):
        if self.object_href:
            return self.object_href.get_absolute_url()
        return self.href

    class Meta:
        verbose_name = "меню(пункт меню)"
        verbose_name_plural = "Навигация"
