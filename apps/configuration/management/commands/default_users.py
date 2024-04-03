import os

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Создаем страндартных пользователей'

    def handle(self, *args, **options):
        User = get_user_model()
        User.objects.create_superuser('content-admin', '', 'PHc7BS7E')
        User.objects.create_superuser('seo-admin', '', 'A1d#m7i*n6')


        print('\n\n------------------------------')
        print('Стандартные пользователи созданы')
        print('------------------------------\n\n')
