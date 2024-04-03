from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class DiscountCard(models.Model):
    """Модель скидочной карты для пользователя личного кабинета."""

    title = models.CharField(
        verbose_name="Наименвоание скидочной карты",
        max_length=150
    )
    percent = models.DecimalField(
        verbose_name="Процент скидки",
        max_digits=4,
        decimal_places=1,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )
    id_1c = models.CharField(
        verbose_name="ИД из 1с",
        max_length=200,
        unique=True
    )

    def __str__(self) -> str:
        return self.title

    @property
    def get_discount(self):
        return self.percent / 100

    class Meta:
        verbose_name = 'Бонусная карта'
        verbose_name_plural = 'Бонусные карты'
