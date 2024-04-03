# -*- coding: UTF-8 -*-
from django.core.management.base import BaseCommand, CommandError
from apps.exchange1c.api import OrderXML
from apps.shop.models import Order

class Command(BaseCommand):
    help = 'Обмен заказами с 1с'

    def handle(self, *args, **options):
        orders = Order.objects.filter(is_imported=False).iterator()
        xml = OrderXML().create(orders, printed=False)
