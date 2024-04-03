from apps.configuration.models import City
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class Vacancy(models.Model):

    title = models.CharField(
        verbose_name="Заголовок",
        default="",
        max_length=300
    )

    text = RichTextUploadingField(
        verbose_name="Текст",
        default=""
    )

    sort = models.IntegerField(
        verbose_name="Сортировка", 
        default=1
    )

    city = models.ForeignKey(City, null=True, blank=True,
                             on_delete=models.SET_NULL,
                             related_name="vacancies",
                             verbose_name="Город")

    def __str__(self):
        return "Вакансия: " + str(self.title)

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"
