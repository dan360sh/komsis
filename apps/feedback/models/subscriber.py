from django.db import models
from django.contrib.auth.models import User


class Subscriber(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, related_name="subscriber")

    def __str__(self):
        return str(self.user.username)

    class Meta:
        verbose_name = 'подписчик'
        verbose_name_plural = 'Подписчики'
