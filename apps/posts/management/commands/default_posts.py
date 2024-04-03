from django.core.management.base import BaseCommand
from django.core.files import File
from django.contrib.auth.models import User
from filer.models import Image
from slugify import slugify

from system import settings
from ...models import Category, Post


class Command(BaseCommand):
    help = 'Получаем дерево каталога, со списком товаров'
    posts = [
        {
            'title': 'Подготовка и выпуск каталога «Застывшие в граните»',
            'description': '',
            'thumbnail': 'new-3.jpg'
        },
        {
            'title': 'Пример новостной статьи с длинным заголовком в ' +
                     'несколько строк',
            'description': '',
            'thumbnail': 'new-2.jpg'
        },
        {
            'title': 'Статья из журнала «Бизнес и Власть»',
            'description': 'Издательское дело-бизнес весьма специфический. ' +
                           'С одной стороны, его владелец должен быть ' +
                           'человеком творческим, креативным. С другой ' +
                           'стороны,-расчетливым, практичным…',
            'thumbnail': 'new-1.jpg'
        }
    ]

    def handle(self, *args, **options):
        self.set_categories()
        self.set_posts()

    def set_categories(self):
        Category.objects.update_or_create(
            title='Новости', defaults=({'title': 'Новости', 'slug': 'news'}))

        print('\n\n------------------------------')
        print('Создана категория: "Новости"')
        print('------------------------------\n\n')

        Category.objects.update_or_create(
            title='Полезные статьи',
            defaults=({'title': 'Полезные статьи', 'slug': 'articles'}))

        print('\n\n------------------------------')
        print('Создана категория: "Полезные статьи"')
        print('------------------------------\n\n')

    def set_posts(self):
        for item in self.posts:
            category = Category.objects.get(title='Новости')
            Post.objects.update_or_create(
                title=item['title'],
                defaults=(
                    {
                        'title': item['title'],
                        'slug': slugify(item['title']),
                        'thumbnail': self.create_image(item['thumbnail']),
                        'category': category,
                        'description': item['description']
                    }
                )
            )

            print('\n\n------------------------------')
            print('Создан пост: ' + item['title'])
            print('------------------------------\n\n')

    def create_image(self, file_name):
        full_path = open(
            settings.BASE_DIR + "/static/images/" + file_name, 'rb')
        file_obj = File(full_path, name="thumbnails - " + file_name)
        user = User.objects.get(username='Admin')

        fields = ({'original_filename': "thumbnails - " + file_name,
                   'owner': user, 'file': file_obj})
        obj, created = Image.objects.get_or_create(
            original_filename="thumbnails - " + file_name, defaults=fields)
        full_path.close()

        return obj
