import re

from apps.seo.models import SeoBase
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.postgres import search
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from filer.fields.file import FilerFileField
from filer.fields.image import FilerImageField

from .. import models as catalog_models


class Brand(SeoBase):
    active = models.BooleanField(verbose_name="Активность", default=True)
    title = models.CharField(verbose_name="Заголовок",
                             blank=False, default="", max_length=300)
    title_upper = models.CharField(verbose_name="Заголовок UPPER", null=True,
                                   blank=False, max_length=300, default=title, db_index=True)
    slug = models.SlugField(verbose_name="Слаг", blank=False,
                            null=True, unique=True, max_length=300)
    thumbnail = FilerImageField(verbose_name="Картинка",
                                null=True, blank=True,
                                related_name="brand_thumbnail",
                                on_delete=models.CASCADE)
    text = RichTextUploadingField(verbose_name="Текст",
                                  blank=True, default="")
    text_upper = RichTextUploadingField(
        verbose_name="Текст UPPER", null=True, blank=False, default=text)

    link = models.CharField(verbose_name='Ссылка',
                            default="", blank=True, max_length=127)
    sort = models.PositiveIntegerField(verbose_name="Сортировка", default=500)

    def __str__(self):
        return self.title_upper

    def get_absolute_url(self):
        return reverse("brand", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = "производитель"
        verbose_name_plural = "Производители"
        ordering = ('sort',)
        indexes = [GinIndex(fields=[
            'title_upper'])]


@receiver(post_save, sender=Brand)
def brandupperizer(sender, instance, **kwargs):
    to_save = False
    upper = instance.title.upper()
    if upper != instance.title_upper:
        instance.title_upper = upper
        to_save = True
    upper = instance.text.upper()
    if upper != instance.text_upper:
        instance.text_upper = upper
        to_save = True
    if to_save:
        instance.save()


class BrandFile(models.Model):
    brand = models.ForeignKey(
        Brand, verbose_name="Блок файлов", related_name="brand_files", on_delete=models.CASCADE)
    obj = FilerFileField(verbose_name="файл",
                         related_name="file_brand", on_delete=models.CASCADE)
    title = models.CharField(verbose_name="Подпись",
                             default="Подпись", max_length=300)

    def __str__(self):
        return "Файл " + str(self.id)

    def get_type(self):
        try:
            return re.search(
                r"\.(.+?)$", self.obj.original_filename).group(1)
        except AttributeError:
            return "File"

    def get_size(self):
        """Получить размер файла поля `obj`.

        Returns:
            `string` -- Размер файла формата: число и единица измерения
        """

        size = self.obj._file_size
        sizes = [" Б", " Кб", " Мб"]
        size_label = sizes[0]
        if size < 100:
            return str(round(size, 2)) + size_label
        size_label = sizes[1]
        size = size / 1024
        if size < 100:
            return str(round(size, 2)) + size_label
        size_label = sizes[2]
        size = size / 1024
        return str(round(size, 2)) + size_label

    class Meta:
        verbose_name = "файл"
        verbose_name_plural = "файлы"
