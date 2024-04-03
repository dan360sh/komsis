from django.core.management.base import BaseCommand, CommandError
from apps.account.models import Account


class Command(BaseCommand):
    help = "Обновить сумму покупок у пользователей"

    def handle(self, *args, **options):
        Account.objects.all().update(purchase_sum=0)
        accounts_list = Account.objects.all()
        for account in accounts_list:
            orders_list = self.get_orders(account)
            result_sum = 0
            for order in orders_list:
                print(f"Номер заказа {order.id}")
                result_sum += order.total
                result_sum = round(result_sum, 2)
                print(f"Сумма, с учетом стоимости текущего заказа {result_sum}")
            account.purchase_sum = result_sum
            account.save()

    def get_orders(self, account):
        # На данный момент, все остальные статусы не работают,
        # поэтому берем заказы только со статусом "В обработке"
        # TODO: Обновить это место сразу после проведения миграций
        return account.orders.filter(status="processing", total__isnull=False)
