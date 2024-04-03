import re
from functools import lru_cache
from typing import Any

from apps.seo.models import SeoBase
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.postgres import search
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.contrib.sitemaps import Sitemap
from django.core.cache import cache
from django.db import models
from django.db.models import Avg, Max, Min, Q, Sum
from django.db.models.functions import Lower
from django.db.models.query import Prefetch
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import get_template
from django.urls import reverse
from django.utils.functional import cached_property
from filer.fields.image import FilerImageField
from mptt.models import MPTTModel, TreeForeignKey

from .. import models as catalog_models
from ..managers import ProductManager
from ..models import Brand, Category, Direction

HIT_MIN = 3

STATUSES = (
    (1, "В наличии"),
    (2, "Ожидается поступление"),
    (3, "Нет в наличии"),
)


class Product(MPTTModel, SeoBase):
    title = models.CharField(verbose_name="Наименование", null=True,
                             blank=False, max_length=3000)

    title_upper = models.CharField(
        verbose_name="Наименование UPPER", null=True, blank=True, db_index=True, max_length=3000)

    active = models.BooleanField(
        verbose_name="Активность", default=True, db_index=True)
    unloading_id = models.CharField('Идентификатор выгрузки', blank=True,
                                    default='', max_length=300)
    slug = models.SlugField(verbose_name='Слаг', blank=True, null=True,
                            unique=True, max_length=255)
    category = models.ForeignKey(Category, verbose_name='Категория',
                                 blank=True, null=True,
                                 related_name='products', on_delete=models.SET_NULL)
    directions = models.ManyToManyField(Direction, verbose_name="Направления",
                                        related_name="direction_products",
                                        blank=True)
    parent = TreeForeignKey('self', verbose_name="Товар-родитель", blank=True,
                            null=True, related_name='product_child', on_delete=models.SET_NULL)
    brand = models.ForeignKey(Brand, verbose_name="Производитель", blank=True,
                              null=True, related_name="brand_products", on_delete=models.SET_NULL)
    thumbnail = FilerImageField(verbose_name="Фотография", null=True,
                                blank=True, related_name="product_thumbnail",
                                on_delete=models.SET_NULL)
    description = RichTextUploadingField(verbose_name="Описание товара",
                                         null=True, blank=True)
    description_upper = RichTextUploadingField(verbose_name="Описание UPPER", null=True, blank=True,
                                               default=description, db_index=True)

    code = models.CharField(verbose_name="Код товара", blank=True,
                            max_length=300, db_index=True)
    status = models.IntegerField(verbose_name="Статус",
                                 choices=STATUSES, default=1)
    price = models.FloatField(verbose_name="Цена", default=0)
    old_price = models.FloatField(verbose_name="Старая цена", default=0)
    wholesale_price = models.FloatField(verbose_name="Оптовая цена", default=0)
    count = models.FloatField(
        verbose_name="Количество", default=0, blank=True)
    # Единица измерения !!!!
    unit = models.CharField(verbose_name="Единица измерения", blank=True,
                            default="", max_length=100)
    step = models.FloatField(verbose_name='Шаг', default=1, )
    new = models.BooleanField(verbose_name="Новинка", default=False)
    hit = models.BooleanField(verbose_name="Хит", default=False)
    sale = models.BooleanField(verbose_name="Распродажа", default=False)
    # Единица измерения 2 ?!?!?!??!?!?!? О_о
    units = models.CharField('Единицы измерения', blank=True,
                             default='', max_length=100)
    count_showing = models.IntegerField(verbose_name="Количество просмотров",
                                        default=0)
    rent = models.BooleanField(verbose_name='Доступна аренда', default=False)
    is_clear_options = models.BooleanField(
        verbose_name="Опции были удалены", default=False, editable=False)
    sort = models.IntegerField("Приоритет", null=True, blank=True)
    vector = SearchVectorField(null=True, editable=False)
    tech_price = models.FloatField(verbose_name="Техническая цена для товара",
                                   default=0)

    objects = models.Manager()
    with_options = ProductManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product', kwargs={'slug': self.slug})

    def get_visible_attrs(self):
        return self.product_attrbutes.filter(group__show=True)

    def _get_total_count(self, attrs):
        result = self.storages.filter(
            **attrs).aggregate(Sum('count'))['count__sum'] or 0
        if str(result).split('.')[-1] == '0':
            return int(result)
        return result

    def get_total_count(self):
        return self._get_total_count({})

    def get_count_vologda(self):
        return self._get_total_count({'storage__title': 'Вологда'})

    def get_count_cherepovets(self):
        return self._get_total_count({'storage__title': 'Череповец'})

    @property
    def display_price(self):
        # логика была такая, если есть Атрибут "Выгружать цену"=0, то цену не показываем при остатке=0
        # В случае с товаром с атрибутом "РАСПРОДАЖА", если остаток=0, то цену не показываем
        # Во всех остальных случаях, если нет запретов, цену показываем
        if self.sale:
            return self.count > 0 and self.price > 0
        else:
            return self.price > 0

    @property
    def default_price(self) -> float:
        price_type = self.prices.filter(
            type__id_1c=catalog_models.DEFAULT_PRICE
        ).first()
        # Если не удалось найти розничную цену
        # возвращается оптовая цена
        return price_type.value if price_type is not None else self.price

    def get_price_by_account(self, account):
        if account is None:
            return self.price

        if account.is_price_type_default:
            return self.price

        prices_by_account = self.prices.filter(type=account.price_type)
        if not prices_by_account.exists():
            return self.price

        price = prices_by_account.first()
        return price.value

    def get_old_price(self, account):
        if account is None:
            return self.old_price
        if account.is_price_type_default:
            return self.old_price

        price = self.prices.filter(type=account.price_type).first()
        return price.old_value if price else 0

    @property
    def is_on_sale(self):
        if self.sale:
            return self.old_price > self.price and self.old_price > 0
        return False

    @property
    def has_on_sale_badge(self):
        return self.sale

    def on_sale(self, account):
        if account is None:
            return self.is_on_sale
        prices_with_old_price = self.prices.filter(
            type=account.price_type,
            old_value__gt=0
        )
        if not prices_with_old_price.exists():
            return False
        price = prices_with_old_price.first()
        return price.old_value > price.value

    @property
    def is_able_to_overflow_count(self):
        """Булево поле инстанса, которое определяет
        может ли быть товар добавлен сверх остатка.

        На данный момент определяется, как наличие свойства у товара
        "ВыгружатьЦену".

        Данное свойство не привязно к товару, как таковое,
        `см. parse.py`.
        В нем, если у товара пришло такое свойство,
        то стоимость этого товара станет 0.

        Returns:
            bool: Наличие или отсутствие свойства 'ВыгружатьЦену'
        """
        return self.price > 0

    def get_available_count(self):
        """Получить кол-во товара для юр. лиц.

        Returns:
            float: Количество товаров
        """
        return 9999

    def get_breadcrumbs(self):
        breadcrumbs = list()
        breadcrumbs.append(self)
        parent = self.parent
        while parent:
            breadcrumbs.append(parent)
            parent = parent.parent
        if self.category:
            return self.category.get_breadcrumbs() + list(reversed(breadcrumbs))
        return breadcrumbs

    def get_pre_category(self):
        category = self.category
        groups = [i[0] for i in list(
            Category.objects.filter(parent=None).values_list('id'))]
        while category.parent and groups.count(category.parent.id) <= 0:
            category = category.parent

        return category

    @cached_property
    def _get_root_category(self):
        return self.category.get_root() if self.category else None

    def get_root_category_title(self):
        category_root = self._get_root_category
        if category_root:
            return self._get_root_category.title

    def get_root_category_id(self):
        category_root = self._get_root_category
        if category_root:
            return self._get_root_category.id

    # @lru_cache(maxsize=64)
    def the_product_card(self, additional=None, request=None):
        return get_template("catalog/product-card.html").render(
            {'product': self, "additional": additional, "request": request})

    def the_product_card_wide(self, additional=None, request=None):
        return get_template("catalog/product-card-wide.html").render(
            {'product': self, "additional": additional, "request": request})

    def first_color(self):
        return self.colors.first()

    def first_option(self):
        return self.options.first()

    def exist_options(self):
        try:
            # может быть аннотировано количество активных опций
            return self._options_exists
        except AttributeError as e:
            pass

        return self.options.filter(active=True).exists()

    def exist_options_stock(self):
        try:
            # может быть аннотировано количество активных опций с количеством
            return self._options_stock_exists
        except AttributeError as e:
            pass

        return self.options.filter(Q(active=True) & Q(count__gt=0)).exists()

    def min_price(self):
        try:
            # может быть аннотирована минимальная стоимость опций
            return self._min_price
        except AttributeError as e:
            pass

        if self.options.filter(active=True, price__gt=0):
            return self.options.filter(active=True, price__gt=0).order_by("price").first().price
        else:
            return None

    def has_count(self):
        # функционал закомментирован из-за излишних запросов
        # теперь общее количество записывается в поле count
        # и наличие проверяется по нему
        # return self.storages.filter(count__gt=0).exists()
        return self.count > 0

    @property
    def is_shock_sale(self) -> bool:
        return self.product_attrbutes.filter(
            Q(group__id=117) & Q(value__id=664)
        ).exists()

    def get_status(self):
        if self.has_count():
            return 'В наличии'
        return 'Ожидается' if self.display_price else 'Нет в наличии'

    def get_variations(self):
        if self.get_children():
            return Product.objects.filter(id=self.id) | self.get_children()
        elif self.parent:
            return Product.objects.filter(id=self.parent.id) | self.parent.get_children()
        else:
            return []

    def get_alt(self):
        if self.thumbnail:
            if self.thumbnail.default_alt_text:
                return self.thumbnail.default_alt_text
            else:
                return self.thumbnail.original_filename
        return ""

    def set_viewed_products(self, request):
        """
                Запись просмотренных товаров в сессию
                """
        try:
            if self.id not in request.session['viewed_products']:
                request.session['viewed_products'].append(int(self.id))
        except KeyError:
            request.session['viewed_products'] = []
            request.session['viewed_products'].append(int(self.id))
        request.session.save()

    def get_viewed_products(self, request):
        """
                Получение просмотренных товаров из сессии
                """
        if request.session.get('viewed_products', False):
            return Product.objects.filter(
                id__in=request.session['viewed_products']).exclude(
                id=self.id)[0:12]
        return None

    def get_similar_items(self):
        if self.category is None:
            return Product.objects.none()
        if self.category.is_root_node():
            filter_cateogries = self.category.get_descendants(
                include_self=True)
        else:
            # get_siblings возвращает TreeQuerySet в котором уже
            # находится текущая категория
            filter_cateogries = self.category.get_siblings

        first_word = self.title.split(" ")[0]

        similars = Product.objects.filter(
            Q(product_child=None) & Q(parent=None) | Q(product_child=None),
            category__in=filter_cateogries,
            active=True,
            price__gte=0,
            count__gte=0,
        ).distinct().exclude(id=self.id).order_by("?").filter(title__icontains=first_word)
        return similars[:12]

    @classmethod
    def get_filters(cls, products, category=None, only_count=False, user=None, request=None):
        """Получение фильтров

                Arguments:
                        products {QuerySet} -- Список товаров

                Returns:
                        dict -- Словарь из фильтров
                """
        # count изменен на exists

        if only_count:
            return {
                "count": products.count(),
                'only_count': True,
                "sale": cls.sale_filter(products).exists(),
                "stock": products.filter(Q(count__gt=0) | Q(options__count__gt=0)).exists(),
                "shock_sale": cls.shock_sale_filter(products).exists(),
            }
        data = {
            "attributes": cls._form_attributes_filter(products, category),
            # "colors": cls._form_colors_filter(products),
            "new": products.filter(new=True).exists(),
            "hit": cls.popular_filter(products).exists(),
            "sale": cls.sale_filter(products).exists(),
            "thumbnail": products.filter(thumbnail__gte=0).exists(),
            "stock": products.filter(Q(count__gt=0) | Q(options__count__gt=0)).exists(),
            # "directions": cls._form_directions_filter(products),
            "brands": cls._form_brands_filter(products),
            "count": products.count(),
            "shock_sale": cls.shock_sale_filter(products).exists(),
        }

        # price_info = products.aggregate(min_value=Min('price'), max_value=Max('price'))
        if user and not user.account.is_price_type_default:
            # QuerySet products уже отфильтрован по нужной цене
            price_info = products.aggregate(min_value=Min(
                'prices__value'), max_value=Max('prices__value'))
        else:
            price_info = products.aggregate(
                min_value=Min('price'), max_value=Max('price'))

        try:
            price_min = int(price_info['min_value'])
        except:
            price_min = 0

        try:
            price_max = int(price_info['max_value'])
        except:
            price_max = 0

        data['price_min'] = price_min
        data['price_max'] = price_max

        available_products = Product.objects.filter(active=True, count__gt=0)
        if category:
            available_products = available_products.filter(
                category__in=category.get_descendants()
            )
        if user and not user.account.is_price_type_default:
            # QuerySet products уже отфильтрован по нужной цене
            available_price_info = available_products.aggregate(min_value=Min(
                'prices__value'), max_value=Max('prices__value'))
        else:
            available_price_info = available_products.aggregate(
                min_value=Min('price'), max_value=Max('price'))

        try:
            data['available_price_min'] = int(
                available_price_info['min_value'])
        except:
            data['available_price_min'] = None

        try:
            data['available_price_max'] = int(
                available_price_info['max_value'])
        except:
            data['available_price_max'] = None

        return data

    # profiling
    # @staticmethod
    # def get_after_filters(products, f_groups=False):
    #     groups = catalog_models.AttributesGroup.objects.filter(
    #         Q(show=True) & Q(Q(attributes__product__in=products) | Q(num_attributes__product__in=products))).distinct()
    #     attributes = list()
    #     filtered_groups = []
    #     for group in groups:
    #         # attrs = cache.get('attrs' + str(group.id))
    #         # if attrs is None:
    #         attrs = list(group.attributes.filter(group__show=True, product__in=products).order_by('value__id').distinct(
    #             'value__id').values_list('name', flat=True))
    #         # cache.set('attrs' + str(group.id), attrs)
    #         attributes += attrs
    #         if f_groups and attrs:
    #             filtered_groups.append(str(group.id))
    #     for d in Direction.objects.filter(direction_products__in=products).distinct():
    #         attributes.append("dir_{}".format(d.id))

    #     for b in Brand.objects.filter(brand_products__in=products).distinct():
    #         attributes.append("brand_{}".format(b.id))

    #     if Product.new_filter(products):
    #         attributes.append('new')
    #     if Product.popular_filter(products):
    #         attributes.append('hit')
    #     if Product.sale_filter(products):
    #         attributes.append('sale')
    #     if products.filter(thumbnail__isnull=False):
    #         attributes.append('thumbnail')
    #     if products.filter(Q(count__gt=0) | Q(options__count__gt=0)):
    #         attributes.append('stock')

    #     if f_groups:
    #         return attributes, filtered_groups
    #     return attributes

    # @classmethod
    # # @lru_cache(maxsize=64)
    # def get_filters(cls, products):
    #	 data = {
    #		 "attributes": cls._form_attributes_filter(products),
    #		 "colors": cls._form_colors_filter(products),
    #		 "new": products.filter(new=True).count(),
    #		 "hit": products.filter(count_showing__gte=HIT_MIN).count(),
    #		 "sale": products.filter(sale=True).count(),
    #		 "thumbnail": products.filter(thumbnail__gte=0).count(),
    #		 "count": products.count()
    #	 }
    #	 return data

    # profiling new
    @staticmethod
    def get_after_filters(products, f_groups=False):
        # groups = catalog_models.AttributesGroup.objects.filter(
        #     Q(show=True) & Q(attributes__product__in=products)).distinct()
        attributes = list()
        filtered_groups = []

        prefetch_values_queryset = (
            catalog_models.
            Attribute.
            objects
            .filter(product__in=products)
            .order_by('value_id')
            .distinct('value_id')
            # .only('pk','name')
        )

        prefetch_values = Prefetch('attributes',
                                   prefetch_values_queryset)

        # получаем атрибуты совместно с их значениями
        groups = (
            catalog_models
            .AttributesGroup
            .objects
            .filter(show=True, attributes__product__in=products)
            .distinct()
            .prefetch_related(prefetch_values))

        for group in groups:
            attrs = [attr.name for attr in group.attributes.all()]
            attributes += attrs
            if f_groups and attrs:
                filtered_groups.append(str(group.id))

        # for d in Direction.objects.filter(direction_products__in=products).distinct():
        #     attributes.append("dir_{}".format(d.id))

        for b in Brand.objects.filter(brand_products__in=products).distinct():
            attributes.append("brand_{}".format(b.id))

        if Product.new_filter(products).exists():
            attributes.append('new')
        if Product.popular_filter(products).exists():
            attributes.append('hit')
        if Product.sale_filter(products).exists():
            attributes.append('sale')
        if products.filter(thumbnail__isnull=False).exists():
            attributes.append('thumbnail')
        if products.filter(Q(count__gt=0) | Q(options__count__gt=0)).exists():
            attributes.append('stock')

        if f_groups:
            return attributes, filtered_groups
        return attributes

    # @staticmethod
    # def get_after_filters(products):
    #	 groups = catalog_models.AttributesGroup.objects.filter(Q(show=True) & Q(Q(attributes__product__in=products) | Q(num_attributes__product__in=products))).distinct()

    #	 attributes = list()
    #	 for group in groups:
    #		 attrs = group.attributes.filter(group__show=True,
    #		 product__in=products).order_by('value', 'sort')
    #		 for attr in attrs:
    #			 attributes.append('ch_' + str(group.id) + '_' + str(attr.value.id))
    #		 if products.filter(new=True):
    #			 attributes.append('new')
    #		 if products.filter(count_showing__gte=HIT_MIN):
    #			 attributes.append('hit')
    #		 if products.filter(Q(old_price__gt=0) | Q(sale=True)):
    #			 attributes.append('sale')
    #		 if products.filter(thumbnail__isnull=False):
    #			 attributes.append('thumbnail')
    #		 if products.filter(count__gte=0):
    #			 attributes.append('stock')

    #	 return attributes

    #   # profiling
    #   @staticmethod
    #   def _form_attributes_filter(products, category):
    #       """Формирование фольтров по атрибутам относительно товаров.

    # Arguments:
    # 	products {QuerySet} -- Список с товарами

    # Returns:
    # 	dict -- Список групп атрибутов
    # """

    #       filters = Q(show=True) & Q(Q(attributes__product__in=products) | Q(num_attributes__product__in=products))
    #       if category and category.parent is None and category.childs.exists():
    #           filters &= Q(show_parent=True)
    #       groups = catalog_models.AttributesGroup.objects.filter(filters).distinct()
    #       attributes = list()

    #       for group in groups:
    #           # l = list(group.attributes.filter(group__show=True, product__in=products).order_by('value__id').distinct(
    #           #     'value__id').values("value__title", "name"))
    #           l = list(group.attributes.filter(group__show=True, product__in=products).order_by('value__title').distinct(
    #               'value__title').values("value__title", "name"))
    #           attributes.append({"group": group.title, "group_id": str(group.id), "attributes": l})
    #       return attributes

    # profiling new
    @staticmethod
    def _form_attributes_filter(products, category):
        """Формирование фольтров по атрибутам относительно товаров.

        Arguments:
            products {QuerySet} -- Список с товарами

        Returns:
            dict -- Список групп атрибутов
        """
        filters = Q(show=True) & Q(attributes__product__in=products)
        if category and category.parent is None and category.childs.exists():
            filters &= Q(show_parent=True)
        # groups = catalog_models.AttributesGroup.objects.filter(filters).distinct()

        prefetch_values_queryset = (
            catalog_models.
            Attribute.
            objects
            .select_related('value')
            .filter(product__in=products)
        )

        prefetch_values = Prefetch('attributes',
                                   prefetch_values_queryset)

        # получаем атрибуты совместно с их значениями
        groups = (
            catalog_models.
            AttributesGroup.
            objects.
            prefetch_related(prefetch_values)
            .filter(filters)
            .distinct())

        attributes = list()

        for group in groups:
            group_with_lower_title = group.attributes.annotate(
                lower_value_title=Lower("value__title"))
            group_with_lower_title = group_with_lower_title.distinct(
                "lower_value_title")
            group_with_lower_title = group_with_lower_title.order_by(
                "lower_value_title")
            l = [{'value__title': attr.value.title, 'name': attr.name}
                 for attr in group_with_lower_title]
            attributes.append(
                {"group": group.title, "group_id": str(group.id), "attributes": l, "show_in_header": group.show_in_header})

        return attributes

    @staticmethod
    def _form_colors_filter(products):
        """Формирование групп цветов относительно товаров.

                Arguments:
                        products {QuerySet} -- Список товаров

                Returns:
                        QuerySet -- Список групп цветов
                """

        color_products = catalog_models.ColorValue.objects.filter(
            colors__product__in=products).distinct()
        # .cache()
        return [{'title': item.title, 'name': 'cg_' + str(item.id),
                 'hex_color': item.hex_color}
                for item in color_products]

    @staticmethod
    def _form_directions_filter(products):
        """Формирование направлений.

                Arguments:
                        products {QuerySet} -- Список товаров

                Returns:
                        QuerySet -- Список направлений
                """
        directions = Direction.objects.filter(
            direction_products__in=products).distinct().order_by('title')
        # .cache()
        return [{'title': item.title, 'name': 'dir_' + str(item.id)} for item in directions]

    @staticmethod
    def _form_brands_filter(products):

        brands = Brand.objects.filter(
            brand_products__in=products).distinct().order_by('title')

        return [{'title': item.title, 'name': 'brand_' + str(item.id)} for item in brands]

    # сложные фильтры
    @staticmethod
    def sale_filter(products):
        return products.filter(Q(old_price__gt=0) | Q(sale=True)).distinct()

    @staticmethod
    def shock_sale_filter(products):
        SHOCK_SALE_QUERY_VALUE = 'ch_117_664'
        return products.filter(
            product_attrbutes__group__id=117,
            product_attrbutes__value__id=664
        )

    @staticmethod
    def new_filter(products):
        return products.filter(Q(new=True))

    @staticmethod
    def popular_filter(products):
        return products.filter(Q(hit=True))

    @staticmethod
    def filter_products(products, request, keep_order=False):
        data = {
            "attributes": list(),
            "directions": list(),
            "brands": list(),
            "groups": set(),
            "colors": list(),
            "thumbnail": False,
            "new": False,
            "hit": False,
            "sale": False,
            "stock": False,
            "search": None,
            "price_min": None,
            "price_max": None,
            "shock_sale": request.GET.get("ch_117_664", None) is not None,
        }

        dict_pattern = r'^ch_(?P<group>\d+)_(?P<value>\d+)$'
        color_pattern = r'^col_(?P<color>\d+)$'
        number_min_pattern = r'^nm_(?P<group>\d+)_i$'
        number_max_pattern = r'^nm_(?P<group>\d+)_a$'
        directions_pattern = r'^dir_(?P<direction>\d+)$'
        brands_pattern = r'^brand_(?P<brand>\d+)$'

        attribute_filters = {}
        num_attribute_filters = {}
        color_filters = []
        direction_filters = []
        brand_filters = []

        # Наполнение фильтров атрибутами
        if request.GET:
            for key, value in request.GET.items():
                attribute = re.match(dict_pattern, key)
                color = re.match(color_pattern, key)
                n_min = re.match(number_min_pattern, key)
                n_max = re.match(number_max_pattern, key)
                direction = re.match(directions_pattern, key)
                brand = re.match(brands_pattern, key)

                # Атрибут строка
                if attribute:
                    attribute_decode = attribute.group("value")
                    if attribute_filters.get(int(attribute.group("group")),
                                             False):
                        attribute_filters[int(attribute.group("group"))] \
                            .append(str(attribute_decode))
                    else:
                        attribute_filters[int(attribute.group("group"))] = [
                            str(attribute_decode)]
                    data["attributes"].append(key)
                elif n_min:
                    attribute_decode = value
                    if num_attribute_filters.get(int(n_min.group("group")), False):
                        num_attribute_filters[int(n_min.group("group"))] \
                            .update({'min': str(attribute_decode)})
                    else:
                        num_attribute_filters[int(n_min.group("group"))] = {
                            'min': str(attribute_decode)}
                    data["attributes"].append(key)
                elif n_max:
                    attribute_decode = value
                    if num_attribute_filters.get(int(n_max.group("group")), False):
                        num_attribute_filters[int(n_max.group("group"))].update(
                            {'max': str(attribute_decode)})
                    else:
                        num_attribute_filters[int(n_max.group("group"))] = {
                            'max': str(attribute_decode)}
                    data["attributes"].append(key)
                elif color:
                    attribute_decode = color.group("color")
                    if not int(attribute_decode) in color_filters:
                        color_filters.append(int(attribute_decode))
                    data["colors"].append(key)
                # elif direction:
                #     attribute_decode = direction.group("direction")
                #     if not int(attribute_decode) in direction_filters:
                #         direction_filters.append(int(attribute_decode))
                #     data['groups'].add("directions")
                #     data["directions"].append(key)
                elif brand:
                    attribute_decode = brand.group("brand")
                    if not int(attribute_decode) in brand_filters:
                        brand_filters.append(int(attribute_decode))
                    data['groups'].add("brands")
                    data["brands"].append(key)

            # Фильтрация товаров относительно атрибутов. Фильтрация ведется
            # по id групп и значений атрибутов.
            for attr in attribute_filters.items():
                data['groups'].add(str(attr[0]))
                products = products.filter(
                    product_attrbutes__group__id=attr[0],
                    product_attrbutes__value__in=attr[1])
            # .cache()
            for attr in num_attribute_filters.items():
                min_value = attr[1].get('min')
                if min_value:
                    min_value = int(min_value)
                else:
                    min_value = 0

                max_value = attr[1].get('max')
                if max_value:
                    max_value = int(max_value)
                else:
                    max_value = 10000000
                products = products.filter(
                    Q(product_num_attrbutes__group__id=attr[0]) & Q(product_num_attrbutes__value__gte=min_value) & Q(
                        product_num_attrbutes__value__lte=max_value))

            # Фильтрация по цветам
            if color_filters:
                products = products.filter(
                    colors__value__id__in=color_filters).distinct()

            if direction_filters:
                products = products.filter(
                    directions__id__in=direction_filters).distinct()

            if brand_filters:
                products = products.filter(
                    brand__id__in=brand_filters).distinct()

            # Проверка дополнительных полей
            price_min: str = request.GET.get("price_min", "")
            price_max: str = request.GET.get("price_max", "")
            price_min, price_max = price_min.replace(
                ' ', ''), price_max.replace(' ', '')
            if price_min:
                data["price_min"] = int(price_min)
            else:
                data["price_min"] = 0
            if price_max:
                data["price_max"] = int(price_max) + 1
            else:
                data["price_max"] = 10000000

            user = request.user if request.user.is_authenticated else None

            if user and not user.account.is_price_type_default:
                products = products.filter(
                    prices__value__gte=data['price_min'], prices__value__lte=data['price_max'])
            else:
                products = products.filter(
                    price__gte=data["price_min"], price__lte=data["price_max"])

            if request.GET.get("thumbnail", "") == "on":
                products = products.filter(thumbnail__gte=0)
                data["thumbnail"] = True
            if request.GET.get("new", "") == "on":
                products = Product.new_filter(products)
                data["new"] = True
            if request.GET.get("hit", "") == "on":
                products = Product.popular_filter(products)
                data["hit"] = True
            if request.GET.get("sale", "") == "on":
                products = Product.sale_filter(products)
                data["sale"] = True
            if request.GET.get("stock", "") == "on":
                products = products.filter(
                    Q(count__gt=0) | Q(options__count__gt=0))
                data["stock"] = True
        sort_p = request.GET.get("sort", 'sort')
        # keep_order сохраняет исходную сортировку (в нашем случае из эластика)
        if not keep_order:
            products = products.order_by(sort_p)
        data['groups'] = list(data['groups'])
        return products, data

    # @staticmethod
    # # @lru_cache(maxsize=64)
    # def filter_products(products, request):
    #	 data = {
    #		 "attributes": [],
    #		 "colors": [],
    #		 "thumbnail": False,
    #		 "new": False,
    #		 "hit": False,
    #		 "sale": False,
    #		 "search": None,
    #		 "price_min": None,
    #		 "price_max": None
    #	 }

    #	 dict_pattern =  r'^ch_(?P<group>\d+)_(?P<value>\d+)$'
    #	 color_pattern =  r'^col_(?P<color>\d+)$'
    #	 number_min_pattern = r'^nm_(?P<group>\d+)_i$'
    #	 number_max_pattern = r'^nm_(?P<group>\d+)_a$'

    #	 attribute_filters = {}
    #	 num_attribute_filters = {}
    #	 color_filters = []

    #	 # Наполнение фильтров атрибутами
    #	 if request.GET:
    #		 for key, value in request.GET.items():
    #			 attribute = re.match(dict_pattern, key)
    #			 color = re.match(color_pattern, key)
    #			 n_min = re.match(number_min_pattern, key)
    #			 n_max = re.match(number_max_pattern, key)

    #			 # Атрибут строка
    #			 if attribute:
    #				 attribute_decode = attribute.group("value")
    #				 if attribute_filters.get(int(attribute.group("group")),
    #										  False):
    #					 attribute_filters[int(attribute.group("group"))]\
    #						 .append(str(attribute_decode))
    #				 else:
    #					 attribute_filters[int(attribute.group("group"))] = [
    #						 str(attribute_decode)]
    #				 data["attributes"].append(key)
    #			 elif n_min:
    #				 attribute_decode = value
    #				 if num_attribute_filters.get(int(n_min.group("group")),False):
    #					 num_attribute_filters[int(n_min.group("group"))]\
    #						 .update({'min' : str(attribute_decode)})
    #				 else:
    #					 num_attribute_filters[int(n_min.group("group"))] = {'min' : str(attribute_decode)}
    #				 data["attributes"].append(key)
    #			 elif n_max:
    #				 attribute_decode = value
    #				 if num_attribute_filters.get(int(n_max.group("group")),False):
    #					 num_attribute_filters[int(n_max.group("group"))].update({'max' : str(attribute_decode)})
    #				 else:
    #					 num_attribute_filters[int(n_max.group("group"))] = {'max' : str(attribute_decode)}
    #				 data["attributes"].append(key)
    #			 elif color:
    #				 attribute_decode = color.group("color")
    #				 if not int(attribute_decode) in color_filters:
    #					 color_filters.append(int(attribute_decode))
    #				 data["colors"].append(key)

    #		 # Фильтрация товаров относительно атрибутов. Фильтрация ведется
    #		 # по id групп и значений атрибутов.
    #		 for attr in attribute_filters.items():
    #			 products = products.filter(
    #				 product_attrbutes__group__id=attr[0],
    #				 product_attrbutes__value__in=attr[1], product_child=None)\
    #				 # .cache()
    #		 for attr in num_attribute_filters.items():
    #			 min_value = attr[1].get('min')
    #			 if min_value:
    #				 min_value = int(min_value)
    #			 else:
    #				 min_value = 0

    #			 max_value = attr[1].get('max')
    #			 if max_value:
    #				 max_value = int(max_value)
    #			 else:
    #				 max_value = 10000000
    #			 products = products.filter(Q(product_num_attrbutes__group__id=attr[0]) & Q(product_num_attrbutes__value__gte=min_value) & Q(product_num_attrbutes__value__lte=max_value))

    #		 # Фильтрация по цветам
    #		 if color_filters:
    #			 products = products.filter(colors__value__id__in = color_filters).distinct()

    #		 # Проверка дополнительных полей
    #		 price_min = request.GET.get("price_min", "")
    #		 price_max = request.GET.get("price_max", "")
    #		 if price_min:
    #			 data["price_min"] = int(price_min)
    #		 else:
    #			 data["price_min"] = 0
    #		 if price_max:
    #			 data["price_max"] = int(price_max)
    #		 else:
    #			 data["price_max"] = 10000000

    #		 products = products.filter(price__gte = data["price_min"], price__lte = data["price_max"])

    #		 if request.GET.get("thumbnail", "") == "on":
    #			 products = products.filter(thumbnail__gte=0)
    #			 data["thumbnail"] = True
    #		 if request.GET.get("new", "") == "on":
    #			 products = products.filter(new=True)
    #			 data["new"] = True
    #		 if request.GET.get("hit", "") == "on":
    #			 products = products.filter(count_showing__gte=HIT_MIN)
    #			 data["hit"] = True
    #		 if request.GET.get("sale", "") == "on":
    #			 products = products.filter(Q(old_price__gt=0) | Q(sale=True))
    #			 data["sale"] = True

    #	 return products, data

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "Товары"
        indexes = [GinIndex(fields=[
            'title',
            'title_upper',
            'description_upper',
            'code'])]
        ordering = ['sort']


# @receiver(post_save, sender=Product)
# def productupperizer(sender, instance, **kwargs):
#     to_save = False
#
#     # обновление полей для поиска, содержащих название в верхнем регистре
#     upper = instance.title.upper()
#     if upper != instance.title_upper:
#         instance.title_upper = upper
#         to_save = True
#     upper = instance.description.upper()
#     if upper != instance.description_upper:
#         instance.description_upper = upper
#         to_save = True
#
#     if to_save:
#         instance.save()

class ProductGallery(models.Model):
    """
        Галерея товаров
        """
    product = models.ForeignKey(Product, verbose_name="Товар", blank=False,
                                null=False, related_name="product_gallery", on_delete=models.CASCADE)
    position = models.PositiveIntegerField(default=1, verbose_name="Позиция")
    photo = FilerImageField(verbose_name="Изображение",
                            null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return "Изображение: " + str(self.photo.name)

    def get_alt(self):
        if self.photo:
            if self.photo.default_alt_text:
                return self.photo.default_alt_text
            else:
                return self.photo.original_filename
        return ""

    class Meta:
        verbose_name = "изображение"
        verbose_name_plural = "Галерея"
        ordering = ['position']


class ProductSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Product.objects.filter(active=True)
