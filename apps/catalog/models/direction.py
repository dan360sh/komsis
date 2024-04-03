from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from filer.fields.image import FilerImageField


class Direction(models.Model):

    title = models.CharField(verbose_name="Наименование", blank=False,
                             null=True, max_length=300, db_index=True)
    title_original = RichTextUploadingField(verbose_name="Оригинальное название",
                                            blank=True, null=True)
    mobile_title = RichTextUploadingField(verbose_name="Название для мобильных телефонов",
                                          blank=True, null=True)
    thumbnail = FilerImageField(verbose_name="Картинка",
                                null=True, blank=True,
                                related_name="direction_thumbnail", on_delete=models.CASCADE)
    mobile_thumbnail = FilerImageField(verbose_name="Картинка для телефонов",
                                       null=True, blank=True,
                                       related_name="direction_thumbnail_mobile", on_delete=models.SET_NULL)
    black_color = models.BooleanField(
        verbose_name="Черный текст в карточке на главной",
        help_text="Иначе белый", default=False)
    sort = models.PositiveIntegerField(verbose_name="Сортировка", default=500)

    def __str__(self):
        return self.title

    def get_title(self) -> str:
        return self.title_original or self.title

    def get_mobile_title(self) -> str:
        return self.mobile_title or self.title

    def get_mobile_thumbnail(self) -> str:
        return self.mobile_thumbnail or self.thumbnail
        # return self.mobile_thumbnail.url() if self.mobile_thumbnail else self.thumbnail.url()

    # def get_products_count(self):
    #     return self.direction_products.filter(active=True).count()

    class Meta:
        verbose_name = "Направление"
        verbose_name_plural = "Направления"
        ordering = ['sort', ]
