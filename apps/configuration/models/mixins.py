from django.db import models


class SortingMixin(models.Model):
    sort = models.IntegerField(verbose_name="Сортировка", default=1)

    class Meta:
        abstract = True
