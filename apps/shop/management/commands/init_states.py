from django.core.management.base import BaseCommand, CommandError
from apps.shop.models import OrderState
from django.db import IntegrityError


class Command(BaseCommand):
    help = "Инициализация состояний заказа"

    def handle(self, *args, **options):
        position = 1
        for set_ in OrderState.CODES:
            code = set_[0]
            title = set_[1]
            try:
                OrderState.objects.create(title=title, code=code,
                                          position=position)
            except IntegrityError:
                pass
            position += 1
