from django.db import models


class Country(models.Model):
    title = models.CharField(verbose_name="Заголовок",
                             default="", max_length=300)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "страна"
        verbose_name_plural = "Страны"
