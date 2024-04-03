from datetime import datetime

from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.core import management
from django.db import models
from django.utils.translation import gettext_lazy as _
from filer.fields.file import FilerFileField
from filer.fields.image import FilerImageField


class Settings(models.Model):

    last_export_date = models.DateTimeField(
        verbose_name="Дата последнего экспорта заказов", default=datetime.now)
    process = models.BooleanField(verbose_name="Идет синхронизация",)
    import_title = models.CharField(
        verbose_name="название файла импорта", max_length=300)
    offers_title = models.CharField(
        verbose_name="название файла цен", max_length=300)

    def __str__(self):
        return str(self.last_export_date)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    class Meta:
        verbose_name = _('Настройки обмена')
        verbose_name_plural = _('Настройки обмена')
