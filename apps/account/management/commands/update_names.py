from django.core.management.base import BaseCommand, CommandError
from apps.account.models import Account


class Command(BaseCommand):
    def handle(self, *args, **options):
        account_list = Account.objects.all()
        for account in account_list:
            clear_name: str = account.surname
            clear_name += " " + account.name
            clear_name += " " + account.middle_name
            account.clear_name = clear_name
            account.save()
