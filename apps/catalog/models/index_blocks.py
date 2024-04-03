from django.db import models
from filer.fields.image import FilerFileField

from apps.configuration.models.mixins import SortingMixin


class IndexBlock(SortingMixin):
    title = models.CharField(verbose_name='Заголовок', max_length=300)
    href = models.CharField(verbose_name='Ссылка', max_length=300)
    is_active = models.BooleanField(
        verbose_name='Отображать блок?', default=True)
    is_clickable = models.BooleanField(
        verbose_name='Ссылка работает?', default=True)
    image_right_bottom = FilerFileField(
        verbose_name='Картинка в правом нижнем углу',
        related_name='index_block_images_right_bottom',
        on_delete=models.CASCADE, null=True
    )
    image_right_top = FilerFileField(
        verbose_name='Картинка в правом верхнем углу',
        related_name='index_block_images_right_top',
        on_delete=models.CASCADE, null=True
    )
    image_left_bottom = FilerFileField(
        verbose_name='Картинка в левом нижнем углу',
        related_name='index_block_images_left_bottom',
        on_delete=models.CASCADE, null=True
    )

    class Meta:
        verbose_name = 'Блок на главной странице'
        verbose_name_plural = 'Блоки на главной странице'

    def __str__(self) -> str:
        return self.title
