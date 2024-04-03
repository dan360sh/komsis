

from django.core.management import BaseCommand
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from apps.catalog.models import Category, Product
from django.db.models import Q, F, Value, CharField, Field
from django.db.models.functions import Upper


def search(search_string):
    up_search = search_string.upper()
    cat = Category.objects
    exclude_category = []
    # Получение неактивных категорий
    for c in cat.iterator():
        # Если категория уже в списке исключенных пропустить
        if c.id in exclude_category:
            continue
        # Если категория неактивна добавить в список неактивных ее и всех ее детей
        if c.active is False:
            exclude_category += list(c.get_children().values_list('id', flat=True))
            exclude_category.append(c.id)
    # Получение фразы на русской и английской раскладке
    ru_search, en_search = translate_search(up_search)

    products = Product.objects \
                   .filter(active=True) \
                   .exclude(category__id__in=exclude_category) \
                   .prefetch_related('brand') \
                   .annotate(
        search=SearchVector(
            'title_upper',
            'description_upper',
            'code',
            'brand__title',
        ),
        similarity=(
                TrigramSimilarity('title_upper', ru_search)
                + TrigramSimilarity('title_upper', en_search)
        )
    ) \
                   .filter(Q(similarity__gt=0.1) | Q(search=ru_search) | Q(search=en_search)) \
                   .order_by('-similarity')[:10] \
        .only('title_upper', 'description_upper', 'code', 'brand__title', 'title')
    print(products)


class Command(BaseCommand):
    help = 'Проверка'

    def handle(self, *args, **options):
        search("Водонагреватель")