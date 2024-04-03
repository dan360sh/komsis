import os

from django.core.management.base import BaseCommand

from system import settings
from django.core.management import call_command
from apps.chronographv2.models import Job
import datetime


class Command(BaseCommand):
    help = 'Вызов процедур создания страндартных страниц'

    def handle(self, *args, **options):
        commands = ['default_users', 'default_settings', 'default_pages', 
                    'default_feedback', 'default_navigation']
        for item in commands:
            try:
                call_command(item)
            except:
                print('======================= увы =======================')

        # Job.objects.create(name='test1',next_run= datetime.datetime(2018, 10, 31, 18, 0, 47), command = 'parse', args="filename=import.xml",frequency="YEARLY")
        # Job.objects.create(name='test2',next_run= datetime.datetime(2018, 10, 31, 18, 0, 47), command = 'parse', args="filename=offers.xml",frequency="YEARLY")