from datetime import date

from apps.configuration.utils import HrefModel, unique_slugify
from apps.content.models import Content
from django.db import models
from django.urls import reverse
from filer.fields.image import FilerImageField


class Offer(models.Model):
    active = models.BooleanField(verbose_name='Опубликован', default=True)
    title = models.CharField(verbose_name='Заголовок', default="", blank=False,
                             max_length=300)
    description = models.TextField(verbose_name="Описание акции", blank=True,
                                   default="")
    slug = models.SlugField(verbose_name='Слаг', blank=False, null=True,
                            unique=True)
    thumbnail = FilerImageField(verbose_name="Минеатюра", null=True, on_delete=models.SET_NULL,
                                blank=True, related_name="offer_thumbnail")
    content = models.ForeignKey(Content, verbose_name="Контент", blank=True,
                                null=True, related_name="offers", on_delete=models.SET_NULL)
    date = models.DateField(
        verbose_name="Дата", blank=True, default=date.today)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # if not self.slug:
        #     self.slug = unique_slugify(self.title, Offer)
        super(Offer, self).save(*args, **kwargs)
        HrefModel.set_object(self)

    def get_absolute_url(self):
        return reverse('offer', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'акция'
        verbose_name_plural = 'Акции'
        ordering = ['-date']
