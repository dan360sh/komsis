from django.db import models
from filer.fields.image import FilerImageField
from ckeditor_uploader.fields import RichTextUploadingField


class SeoBase(models.Model):
    seo_text = RichTextUploadingField(verbose_name="Текст",
                                      null=True, blank=True)
    seo_img = FilerImageField(verbose_name="Изображение",
                              null=True, blank=True,
                              related_name="%(app_label)s_%(class)s_seo_img")
    meta_title = models.CharField(verbose_name="SEO заголовок", default='',
                                  blank=True, max_length=300)
    meta_description = models.TextField(verbose_name="Meta Description",
                                        null=True, blank=True)
    meta_keywords = models.TextField(verbose_name="Meta Keywords",
                                     null=True, blank=True)

    class Meta:
        abstract = True
