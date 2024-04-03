from django.core.management.base import BaseCommand
from django.core.files import File
from django.contrib.auth.models import User
from filer.models import Image
from slugify import slugify

from system import settings
from ...models import Page


class Command(BaseCommand):
    help = 'Создание стаднартных страниц'
    pages = [
        {
            'parent': None,
            'title': 'О компании'
        },
        {
            'parent': 'О компании',
            'title': 'Шоурум'
        },
        {
            'parent': 'О компании',
            'title': 'Наша команда'
        },
        {
            'parent': 'О компании',
            'title': 'Клиенты'
        },
        {
            'parent': 'О компании',
            'title': 'Новости'
        },
        {
            'parent': 'О компании',
            'title': 'Награды и благодарности'
        },
        {
            'parent': None,
            'title': 'Клиентам'
        },
        {
            'parent': 'Клиентам',
            'title': 'Доставка и оплата'
        },
        {
            'parent': 'Клиентам',
            'title': 'Технические требования к макетам'
        },
        {
            'parent': 'Клиентам',
            'title': 'Терминология'
        },
        {
            'parent': 'Клиентам',
            'title': 'Полезные статьи'
        }
    ]

    def handle(self, *args, **options):
        # Простые страницы
        for item in self.pages:
            if item['parent']:
                parent = Page.objects.get(title=item['parent'])
            else:
                parent = None
            fields = ({'title': item['title'], 'parent': parent,
                       'slug': slugify(item['title'])})
            Page.objects.update_or_create(title=item['title'], defaults=fields)

            print('\n\n------------------------------')
            print(item['title'])
            print('------------------------------\n\n')


        return obj
