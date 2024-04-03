import timeit
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command


class Command(BaseCommand):
    def handle(self, *args, **options):
        start = timeit.default_timer()
        call_command("search_index", "--rebuild")
        stop = timeit.default_timer()
        print("Time: ", round(stop - start, 5))
