from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import datetime
import traceback


class Email(models.Model):
    title = models.CharField(max_length=300, default="", verbose_name='Email')

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'email'
        verbose_name_plural = 'Emails'

class serviceEmail(models.Model): # derived because Email objects already used everywhere in whole w/o filtering
    title = models.CharField(max_length=300, default="", verbose_name='Email')
    subscription_exchange = models.BooleanField(default=False, verbose_name='subscription to 1C exchange service notifications')

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'service email'
        verbose_name_plural = 'service emails'


class LoggingEmail(models.Model):
    date = models.DateTimeField(verbose_name="Дата отправки")
    to = models.EmailField(verbose_name="Адреса получателей")
    subject = models.CharField(max_length=200, verbose_name="Заголовок письма")
    ok = models.BooleanField(default=False, verbose_name="Письмо отправлено")
    exception_body = models.TextField(null=True, blank=True,
                                      verbose_name="Вывод ошибки")
    result = models.TextField(null=True, blank=True,
                              verbose_name="Отчет об отправке")

    def __str__(self) -> str:
        return self.subject

    def set_error_body(self, exception: Exception):
        result = str(exception)
        for row in traceback.format_tb(exception.__traceback__):
            result += "\n" + row
        self.exception_body = result
        self.save()

    class Meta:
        verbose_name = "Отчет об отправленном письме"
        verbose_name_plural = "Отчеты об отправленных письмах"


@receiver(pre_save, sender=LoggingEmail)
def email_pre_save_receiver(sender, instance, **kwargs):
    if instance.id is None:
        instance.date = datetime.now()
