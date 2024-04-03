import re

from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.postgres.indexes import GinIndex
from django.contrib.sitemaps import Sitemap
from django.db import models
from django.db.models import Max, Min, Q
from django.urls import reverse
from django.utils.functional import cached_property
from filer.fields.image import FilerImageField
from mptt.models import MPTTModel, TreeForeignKey

from apps.configuration.utils import HrefModel
from apps.seo.models import SeoBase

from .. import models as catalog_models

# from functools import lru_cache


HIT_MIN = 3


class Category(MPTTModel, SeoBase):
    active = models.BooleanField(verbose_name="Активность", default=True)
    unloading_id = models.CharField(
        "Идентификатор выгрузки", blank=True, default="", max_length=300
    )
    title = models.CharField(
        verbose_name="Наименование",
        blank=False,
        null=True,
        max_length=300,
        db_index=True,
    )
    slug = models.SlugField(
        verbose_name="Слаг", blank=False, null=True, unique=True, max_length=300
    )
    parent = TreeForeignKey(
        "self",
        verbose_name="Родитель",
        blank=True,
        null=True,
        related_name="childs",
        on_delete=models.CASCADE,
    )
    thumbnail = FilerImageField(
        verbose_name="Миниатюра",
        null=True,
        blank=True,
        related_name="category_thumbnail",
        on_delete=models.CASCADE,
    )
    description = RichTextUploadingField(
        verbose_name="Описание", blank=True, default=""
    )
    black_color = models.BooleanField(
        verbose_name="Черный текст в карточке на главной",
        help_text="Иначе белый",
        default=False,
    )
    display_nested_filters = models.BooleanField(
        verbose_name="Отображать фильтрацию вложенных категорий", default=False
    )
    alt_title = models.CharField(
        verbose_name="Альтернативное наименование",
        help_text="""Заголовок, который
                                            будет выводиться на страницах,
                                            прим. страница с направлениями""",
        max_length=200,
        null=True,
        blank=True,
    )
    display_related_categories_and_filters = models.BooleanField(
        verbose_name="Показывать кнопки фильтров в заголовке каталога",
        default=True,
    )
    display_related_categories = models.BooleanField(
        verbose_name="Показывать кнопки категорий в заголовке каталога",
        default=True,
    )
    display_in_categories = models.BooleanField(
        default=True,
        verbose_name="Отображать в списке категорий",
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # if not self.slug:
        #     self.slug = unique_slugify(self.title, Category)
        super(Category, self).save(*args, **kwargs)
        HrefModel.set_object(self)

    def get_absolute_url(self):
        return reverse("product-category", kwargs={"slug": self.slug})

    # def get_breadcrumbs(self):
    #     breadcrumbs = list()
    #     breadcrumbs.append(self)
    #     parent = self.parent
    #     while parent:
    #         breadcrumbs.append(parent)
    #         parent = parent.parent
    #     breadcrumbs.append({'title':'Каталог','get_absolute_url':'/product-category/'})
    #     breadcrumbs.append({'title':'Главная','get_absolute_url':'/'})
    #     return list(reversed(breadcrumbs))

    def get_breadcrumbs(self):
        breadcrumbs = list()
        breadcrumbs.append({"title": "Главная", "get_absolute_url": "/"})
        breadcrumbs.append(
            {"title": "Каталог", "get_absolute_url": "/product-category/"}
        )
        for parent in self.get_ancestors():
            breadcrumbs.append(parent)
        breadcrumbs.append(self)

        return list(breadcrumbs)

    @cached_property
    def get_siblings(self):
        if self.parent:
            return self.parent.get_children().filter(display_in_categories=True)
        childs = self.childs.filter(active=True, display_in_categories=True).order_by("title")
        if childs:
            return childs
        return []
        # return Category.objects.filter(parent=None, active=True)

    @classmethod
    # @lru_cache(maxsize=64)
    def get_products(cls, category, random=False, salemode=False):
        query = catalog_models.Product.with_options.filter(
            category__in=category.get_descendants(include_self=True),
            active=True,
            parent=None,
        )

        if salemode:
            query = query.filter(Q(old_price__gt=0) | Q(sale=True))
        query = query.distinct()
        if random:
            return query.order_by("?")
        return query.order_by("sort", "-id", "thumbnail")

    @classmethod
    def get_products_query(cls, category, random=False, salemode=False):
        query = {
            "category__in": category.get_descendants(include_self=True),
            "active": True,
            "parent": None,
        }

        return query

    # @lru_cache(maxsize=64)
    def get_products_count(self):
        return self.get_products(self).count()

    def get_products_count_sale(self):
        return self.get_products(self, salemode=True).count()

    # @lru_cache(maxsize=64)
    def get_filters(self, products):
        """Получение фильтров

        Arguments:
            products {QuerySet} -- Список товаров

        Returns:
            dict -- Словарь из фильтров
        """
        price_info = products.aggregate(min_value=Min("price"), max_value=Max("price"))
        try:
            price_min = int(price_info["min_value"])
        except:
            price_min = 0

        try:
            price_max = int(price_info["max_value"])
        except:
            price_max = 0
        data = {
            "attributes": self._form_attributes_filter(products),
            "colors": self._form_colors_filter(products),
            "new": products.filter(new=True).count(),
            "hit": products.filter(count_showing__gte=HIT_MIN).count(),
            "sale": products.filter(Q(old_price__gt=0) | Q(sale=True)).count(),
            "thumbnail": products.filter(thumbnail__gte=0).count(),
            "stock": products.filter(count__gte=0).count(),
            "price_min": price_min,
            "price_max": price_max,
            "count": products.count(),
        }
        return data

    def get_after_filters(self, products):
        groups = catalog_models.AttributesGroup.objects.filter(
            Q(show=True)
            & Q(
                Q(attributes__product__in=products)
                | Q(num_attributes__product__in=products)
            )
        ).distinct()

        attributes = list()
        for group in groups:
            attrs = group.attributes.filter(
                group__show=True, product__in=products
            ).order_by("value", "sort")
            for attr in attrs:
                attributes.append("ch_" + str(group.id) + "_" + str(attr.value.id))
            if products.filter(new=True):
                attributes.append("new")
            if products.filter(count_showing__gte=HIT_MIN):
                attributes.append("hit")
            if products.filter(Q(old_price__gt=0) | Q(sale=True)):
                attributes.append("sale")
            if products.filter(thumbnail__isnull=False):
                attributes.append("thumbnail")
            if products.filter(count__gte=0):
                attributes.append("stock")

        return attributes

    def _form_attributes_filter(self, products):
        """Формирование фольтров по атрибутам относительно товаров.

        Arguments:
            products {QuerySet} -- Список с товарами

        Returns:
            dict -- Список групп атрибутов
        """

        groups = catalog_models.AttributesGroup.objects.filter(
            Q(show=True)
            & Q(
                Q(attributes__product__in=products)
                | Q(num_attributes__product__in=products)
            )
        ).distinct()

        attributes = list()
        for group in groups:
            attributes.append(group.search_attributes(products))
        return attributes

    def _form_colors_filter(self, products):
        """Формирование групп цветов относительно товаров.

        Arguments:
            products {QuerySet} -- Список товаров

        Returns:
            QuerySet -- Список групп цветов
        """

        color_products = catalog_models.ColorValue.objects.filter(
            colors__product__in=products
        ).distinct()
        # .cache()
        return [
            {
                "title": item.title,
                "name": "col_" + str(item.id),
                "hex_color": item.hex_color,
            }
            for item in color_products
        ]

    def filter_products(self, products, request):
        data = {
            "attributes": [],
            "colors": [],
            "thumbnail": False,
            "new": False,
            "hit": False,
            "sale": False,
            "search": None,
            "price_min": None,
            "price_max": None,
        }

        dict_pattern = r"^ch_(?P<group>\d+)_(?P<value>\d+)$"
        color_pattern = r"^col_(?P<color>\d+)$"
        number_min_pattern = r"^nm_(?P<group>\d+)_i$"
        number_max_pattern = r"^nm_(?P<group>\d+)_a$"

        attribute_filters = {}
        num_attribute_filters = {}
        color_filters = []

        # Наполнение фильтров атрибутами
        if request.GET:
            for key, value in request.GET.items():
                attribute = re.match(dict_pattern, key)
                color = re.match(color_pattern, key)
                n_min = re.match(number_min_pattern, key)
                n_max = re.match(number_max_pattern, key)

                # Атрибут строка
                if attribute:
                    attribute_decode = attribute.group("value")
                    if attribute_filters.get(int(attribute.group("group")), False):
                        attribute_filters[int(attribute.group("group"))].append(
                            str(attribute_decode)
                        )
                    else:
                        attribute_filters[int(attribute.group("group"))] = [
                            str(attribute_decode)
                        ]
                    data["attributes"].append(key)
                elif n_min:
                    attribute_decode = value
                    if num_attribute_filters.get(int(n_min.group("group")), False):
                        num_attribute_filters[int(n_min.group("group"))].update(
                            {"min": str(attribute_decode)}
                        )
                    else:
                        num_attribute_filters[int(n_min.group("group"))] = {
                            "min": str(attribute_decode)
                        }
                    data["attributes"].append(key)
                elif n_max:
                    attribute_decode = value
                    if num_attribute_filters.get(int(n_max.group("group")), False):
                        num_attribute_filters[int(n_max.group("group"))].update(
                            {"max": str(attribute_decode)}
                        )
                    else:
                        num_attribute_filters[int(n_max.group("group"))] = {
                            "max": str(attribute_decode)
                        }
                    data["attributes"].append(key)
                elif color:
                    attribute_decode = color.group("color")
                    if int(attribute_decode) not in color_filters:
                        color_filters.append(int(attribute_decode))
                    data["colors"].append(key)

            # Фильтрация товаров относительно атрибутов. Фильтрация ведется
            # по id групп и значений атрибутов.
            for attr in attribute_filters.items():
                products = products.filter(
                    product_attrbutes__group__id=attr[0],
                    product_attrbutes__value__in=attr[1],
                )
                # .cache()
            for attr in num_attribute_filters.items():
                min_value = attr[1].get("min")
                if min_value:
                    min_value = int(min_value)
                else:
                    min_value = 0

                max_value = attr[1].get("max")
                if max_value:
                    max_value = int(max_value)
                else:
                    max_value = 10000000
                products = products.filter(
                    Q(product_num_attrbutes__group__id=attr[0])
                    & Q(product_num_attrbutes__value__gte=min_value)
                    & Q(product_num_attrbutes__value__lte=max_value)
                )

            # Фильтрация по цветам
            if color_filters:
                products = products.filter(
                    colors__value__id__in=color_filters
                ).distinct()

            # Проверка дополнительных полей
            price_min = request.GET.get("price_min", "")
            price_max = request.GET.get("price_max", "")
            if price_min:
                data["price_min"] = int(price_min)
            else:
                data["price_min"] = 0
            if price_max:
                data["price_max"] = int(price_max)
            else:
                data["price_max"] = 10000000

            products = products.filter(
                price__gte=data["price_min"], price__lte=data["price_max"]
            )

            if request.GET.get("thumbnail", "") == "on":
                products = products.filter(thumbnail__gte=0)
                data["thumbnail"] = True
            if request.GET.get("new", "") == "on":
                products = products.filter(new=True)
                data["new"] = True
            if request.GET.get("hit", "") == "on":
                products = products.filter(count_showing__gte=HIT_MIN)
                data["hit"] = True
            if request.GET.get("sale", "") == "on":
                products = products.filter(Q(old_price__gt=0) | Q(sale=True))
                data["sale"] = True

        return products, data

    class MPTTMeta:
        order_insertion_by = ["title"]

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "Категории"
        indexes = [GinIndex(fields=["title"])]


class CategorySitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Category.objects.filter(active=True)
        return Category.objects.filter(active=True)
