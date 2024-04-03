from django.db import models


class CourierCity(models.Model):
    """
    Модель городов курьерской доставки
    """

    name = models.CharField(verbose_name="Имя нас. пункта",blank=False, 
                            max_length=100)
   

    def __str__(self):
        return  self.name 

    class Meta:
        verbose_name = 'Город для курьерской доставки'
        verbose_name_plural = 'Города для курьерской доставки'