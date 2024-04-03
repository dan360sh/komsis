# import os
# from typing import Optional, TextIO

# from django.core.management.base import BaseCommand
# from system import settings

# from ...models import Settings, TypeShipping


# class Command(BaseCommand):
#     help = 'Получаем дерево каталога, со списком товаров'

#     def __init__(self, stdout: Optional[TextIO] = ..., stderr: Optional[TextIO] = ..., no_color: bool = ..., force_color: bool = ...) -> None:
#         super().__init__(stdout, stderr, no_color, force_color)
#         self.seo_text = open(os.path.join(settings.BASE_DIR, 'apps', 'configuration',
#                                           'management', 'commands', 'seo-text.html'))
#         self.privacy_policy = open(os.path.join(settings.BASE_DIR, 'apps',
#                                                 'configuration', 'management',
#                                                 'commands', 'privacy-policy.html'))

#     robots_txt = "User-Agent: * \n\
#                   Disallow: /"

#     def handle(self, *args, **options):
#         Settings.objects.update_or_create(
#             language=settings.LANGUAGES[0][0],
#             defaults=({
#                 'language': settings.LANGUAGES[0][0],
#                 'name': 'Placestart',
#                 'full_address': 'г. Вологда ул. Ленинградская 71к2',
#                 'address': 'г. Вологда ул. Ленинградская 71к2',
#                 'phones': '+7 (999) 111-93-36',
#                 'time_work': 'Пн-Пт с 8:00 до 21:00',
#                 'coord_x': '61.236809',
#                 'coord_y': '46.641949',
#                 'vkontakte': 'https://vk.com/placestart',
#                 'seo_text': str(self.seo_text.read()),
#                 'privacy_policy': str(self.privacy_policy.read()),
#                 'robots_txt': self.robots_txt
#             })
#         )

#         print('\n\n------------------------------')
#         print('Стандартные настройки созданы')
#         print('------------------------------\n\n')

#         TypeShipping.objects.update_or_create(
#             title="Самовывоз",
#             show_address=False,
#             calculation='price_fix',
#             price_fix=0,
#             price_km=0,
#         )

#         TypeShipping.objects.update_or_create(
#             title="Транспортной компанией",
#             show_address=True,
#             calculation='price_km',
#             price_fix=0,
#             price_km=50,
#             cities_free="Вологда"
#         )

#         TypeShipping.objects.update_or_create(
#             title="Почтой россии",
#             show_address=True,
#             calculation='price_fix',
#             price_fix=500,
#             price_km=0,
#         )

#         TypeShipping.objects.update_or_create(
#             title="Курьером",
#             show_address=True,
#             calculation='price_fix',
#             price_fix=1500,
#             price_km=0,
#             cities="Вологда",
#         )
