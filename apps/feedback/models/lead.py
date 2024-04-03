from django.db import models


class Lead(models.Model):
    name = models.CharField(max_length=300, default="", verbose_name='Имя')
    email = models.CharField(max_length=300, default="", verbose_name='Email')
    message = models.CharField(max_length=300, default="", verbose_name='Сообщение')

    def __str__(self):
        return str(self.name + self.email) 

    class Meta:
        verbose_name = 'Лид'
        verbose_name_plural = 'Лиды'
