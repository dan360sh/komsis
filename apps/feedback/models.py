from django.db import models


class ContactForms(models.Model):
    pass


class Email(models.Model):
    title = models.CharField(max_length=300, default="", verbose_name='Email')

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'email'
        verbose_name_plural = 'Emails'
