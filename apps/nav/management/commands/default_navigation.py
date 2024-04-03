from django.core.management.base import BaseCommand
from django.core.files import File
from django.contrib.auth.models import User
from filer.models import Image
from slugify import slugify

from system import settings
from apps.nav.models import Navigation
from apps.pages.models import Page


class Command(BaseCommand):
    help = 'Создание стаднартных страниц'
    navs = [
        {
            'title':'general-menu',
            'alias':'general-menu',
            'parent':None,
            'href':""
        },
        {
            'title':'sidebar-menu',
            'alias':'sidebar-menu',
            'parent':None,
            'href':""
        },
        {
            'parent': 'sidebar-menu',
            'title': 'О компании',
            'href': 'О компании'
        },
        {
            'parent': 'general-menu',
            'title': 'О компании',
            'href': 'О компании'
        },

    ]



    def handle(self, *args, **options):
        for item in self.navs:
            if item['parent']:
                parent = Navigation.objects.get(title=item['parent'])
            else:
                parent = None
            if item['href']:
                try:
                    item['href'] = Page.objects.get(title=item['href']).get_absolute_url()
                except:
                    item['href'] = "#"
            # print(item)
            Navigation.objects.update_or_create(title=item['title'], defaults=item)

            print('\n\n------------------------------')
            print(item['title'])
            print('------------------------------\n\n')


        # return obj
