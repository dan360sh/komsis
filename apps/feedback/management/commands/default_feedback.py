import os

from django.core.management.base import BaseCommand

from system import settings
from apps.feedback.models import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        Email.objects.create(title='feadback@place-start.ru')

        print('\n\n------------------------------')
        print('Стандартный email для обратной связи')
        print('------------------------------\n\n')
