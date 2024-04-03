from apps.configuration.utils import HrefModel, unique_slugify
from apps.content.models import Content
from apps.seo.models import SeoBase
from django.db import models
from django.urls import reverse
from filer.fields.image import FilerImageField
from mptt.models import MPTTModel, TreeForeignKey

TEMPLATE_TYPES = (
    (0, 'Обычная'),
    (1, 'Акции'),
    (2, 'Контакты')
)


class Page(MPTTModel, SeoBase):
    active = models.BooleanField(verbose_name='Опубликован', default=True)
    title = models.CharField(verbose_name='Заголовок', default="", blank=False,
                             max_length=300)
    slug = models.SlugField(verbose_name='Слаг', blank=False, null=True,
                            unique=True)
    parent = TreeForeignKey('self', verbose_name="Родитель",
                            related_name="childs", null=True, blank=True, on_delete=models.SET_NULL)
    thumbnail = FilerImageField(verbose_name="Минеатюра", null=True,
                                blank=True, related_name="page_thumbnail", on_delete=models.SET_NULL)
    original = models.ForeignKey(HrefModel, verbose_name="Оригинал",
                                 blank=True, null=True, on_delete=models.SET_NULL)
    content = models.ForeignKey(Content, verbose_name="Контент", blank=True,
                                null=True, related_name="pages", on_delete=models.SET_NULL)
    template = models.IntegerField(
        verbose_name="Шаблон", choices=TEMPLATE_TYPES, default=0)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # if not self.slug:
        #     self.slug = unique_slugify(self.title, Page)
        super(Page, self).save(*args, **kwargs)
        HrefModel.set_object(self)

    def get_absolute_url(self):
        if self.template > 0:
            if self.template == 1:
                return reverse('offers')
            elif self.template == 2:
                return reverse('contacts')
        else:
            if self.original:
                return self.original.get_absolute_url()
            return reverse('page', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'страница'
        verbose_name_plural = 'Страницы'
