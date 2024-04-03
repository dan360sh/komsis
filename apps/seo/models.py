from django.db import models
from filer.fields.image import FilerImageField
from ckeditor_uploader.fields import RichTextUploadingField


class SeoBase(models.Model):
    seo_text = RichTextUploadingField(verbose_name="Текст",
                                      null=True, blank=True)
    # seo_img = FilerImageField(verbose_name="Изображение",
    #                           null=True, blank=True,
    #                           related_name="%(app_label)s_%(class)s_seo_img")
    seo_text = RichTextUploadingField(verbose_name="SEO текст", default="",
                                      blank=True)
    seo_img1 = FilerImageField(verbose_name="SEO картинка 1", null=True,
                              blank=True, related_name="%(app_label)s_%(class)s_seo_img1",
                              on_delete=models.SET_NULL)
    seo_img2 = FilerImageField(verbose_name="SEO картинка 2", null=True,
                              blank=True, related_name="%(app_label)s_%(class)s_seo_img2",
                              on_delete=models.SET_NULL)
    seo_img3 = FilerImageField(verbose_name="SEO картинка 3", null=True,
                              blank=True, related_name="%(app_label)s_%(class)s_seo_img3",
                              on_delete=models.SET_NULL)
    meta_title = models.CharField(verbose_name="SEO заголовок", default='',
                                  blank=True, max_length=300)
    meta_description = models.TextField(verbose_name="Meta Description",
                                        null=True, blank=True)
    meta_keywords = models.TextField(verbose_name="Meta Keywords",
                                     null=True, blank=True)

    class Meta:
        abstract = True
