from django.db import models


class Manager(models.Model):
    """Модель менеджера для пользователя личного кабинета"""

    name = models.CharField(verbose_name='ФИО', max_length=100)
    phone = models.CharField('Номер телефона', max_length=100)
    email = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Менеджер'
        verbose_name_plural = 'Менеджеры'
