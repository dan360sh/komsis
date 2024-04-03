import itertools
import re
import string
from collections import Counter

from django.contrib.postgres.search import (
    SearchQuery,
    SearchRank,
    SearchVector,
    TrigramSimilarity,
)
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from django.db.models import Case, CharField, F, Field, IntegerField, Q, Value, When
from django.db.models.functions import Greatest, Substr, Upper
from django.http import Http404, JsonResponse
from django.template.loader import get_template
from django.views.generic import TemplateView, View
from django.views.generic.detail import DetailView, SingleObjectTemplateResponseMixin
from django.views.generic.list import ListView

from apps.configuration.models import Settings
from apps.configuration.utils import format_word, pagination
from apps.configuration.views import JSONDetailView, JSONResponseMixin
from apps.elastic_search.search import (
    get_search_query,
    search_elastic,
    search_elastic_queryset,
)
from apps.shop.models import Compare, Favorites

from .models import Brand, Category, Direction, Product


class CatalogList(ListView):
    model = Category
    context_object_name = "catalog"
    template_name = "catalog/catalog.html"
    try:
        queryset = model.objects.filter(active=True, parent=None).order_by("title")
    except ObjectDoesNotExist:
        queryset = False


class DirectionCategoryList(ListView):
    model = Direction
    context_object_name = "direction_categories"
    template_name = "catalog/direction.html"

    def get_queryset(self):
        dir_id = self.args[0].replace("dir_", "")
        self.direction = self.model.objects.get(id=dir_id)
        # return direction.direction_products.order_by('category').distinct('category')
        return set(
            [
                i.get_pre_category()
                for i in self.direction.direction_products.filter(active=True)
                .order_by("category")
                .distinct("category")
            ]
        )

    def get_context_data(self, **kwargs):
        context = super(DirectionCategoryList, self).get_context_data(**kwargs)
        context["direction"] = self.direction
        return context


class ActionCategoryList(ListView):
    model = Category
    context_object_name = "categories"
    template_name = "catalog/actions.html"

    def get_queryset(self):
        action_products = Product.sale_filter(Product.objects.filter(active=True))
        # return direction.direction_products.order_by('category').distinct('category')
        return set(
            [
                product.get_pre_category()
                for product in action_products.order_by("category").distinct("category")
            ]
        )


class CategoryList(ListView):
    model = Category
    context_object_name = "category_list"
    template_name = "catalog/category-list.html"

    def get_queryset(self):
        product_filter = {
            "new": Product.new_filter,
            "hit": Product.popular_filter,
        }[self.kwargs["type"]]

        products = product_filter(Product.objects.filter(active=True))

        return set(
            [
                product.get_pre_category()
                for product in products.order_by("category").distinct("category")
            ]
        )

    def get_context_data(self, **kwargs):
        context = super(CategoryList, self).get_context_data(**kwargs)
        context["filter"] = {
            "new": "new=on",
            "hit": "hit=on",
        }[self.kwargs["type"]]
        return context


class CategoryJSONDetail(SingleObjectTemplateResponseMixin, JSONDetailView):
    model = Category
    context_object_name = "product-category"
    template_name = "catalog/category.html"

    def render_to_response(self, context, **response_kwargs):
        obj: Category = context["object"]
        request = self.request
        products = self.model.get_products(obj, salemode=request.GET.get("sale"))
        user = request.user
        if request.user.is_authenticated:
            if not user.account.is_price_type_default:
                products = products.filter(prices__type=user.account.price_type)
        only_count = False
        if obj.parent is None and obj.childs.exists() is True:
            only_count = True
            if obj.display_nested_filters:
                only_count = False
        filtered_groups = []
        if self.request.GET.get("ajax") == "Y":
            user = user if user.is_authenticated else None
            context["filters"] = Product.get_filters(
                products, obj, only_count=only_count, user=user
            )
            products, context["active"] = Product.filter_products(products, request)
            context["filtration_after"], filtered_groups = Product.get_after_filters(
                products, True
            )
        context["word"] = format_word(obj.get_products_count())
        web_settings = Settings.objects.filter(language=request.LANGUAGE_CODE).first()
        if not web_settings:
            web_settings = Settings.objects.first()
            if not web_settings:
                web_settings = Settings(language="fallback")

        # card_type = request.GET.get("type","tile")
        card_type = request.session.get("card_type", "")
        # card_type = request.GET.get("card_type","tile")
        context["tile"] = card_type == "tile"

        # Пагинация и кнопка показать еще

        if self.request.GET.get("ajax") == "Y":
            count_products = products.count()
            if count_products:
                try:
                    page = int(request.GET.get("page", 1))
                except:
                    page = 1

                if int(count_products) <= int(12):
                    # context['more_button'] = ""
                    context["pagination"] = ""
                else:
                    products = products.annotate_options()
                    pagin = pagination(products, page, 12, count=count_products)
                    products = pagin.items
                    context["pagination"] = get_template(
                        "catalog/includes/pagination.html"
                    ).render({"PAGIN": pagin})
            else:
                count_products = 0

            # Удаление лишних объектов
            del (context["object"], context["product-category"], context["view"])

            # sale_category_list = obj.get_descendants(include_self=True)
            # sale_category_list = Category.objects.filter(active=True)
            if "salemode" in request.GET.keys():
                sale_products = Product.sale_filter(Product.objects.filter(active=True))
                sale_category_list = (
                    sale_products.order_by("category")
                    .distinct("category")
                    .values_list("category", flat=True)
                )
                sale_category_set = set()
                for sale_category in sale_category_list:
                    sale_category_set.update(
                        Category.objects.get(id=sale_category)
                        .get_ancestors(include_self=True)
                        .values_list("id", flat=True)
                    )
                sale_category_list = Category.objects.filter(id__in=sale_category_set)
            else:
                sale_category_list = False
            print(sale_category_list)
            context["template_filters"] = get_template(
                "catalog/includes/filters.html"
            ).render(
                {
                    "filters": context["filters"],
                    "category": obj,
                    "active": context["active"],
                    "filtration_after": context["filtration_after"],
                    "settings": web_settings,
                    "count_products": count_products,
                    "filtered_groups": filtered_groups,
                    "sale_category_list": sale_category_list,
                    "in_category": True,
                    "only_count": only_count,
                }
            )

            # Добавление иконок
            additional = {}
            if request.user.is_authenticated:
                try:
                    # additional['favorites_list'] = [item.product.id for item in
                    #                                 Favorites.objects.get(account__user=request.user).items()]
                    additional[
                        "favorites_list"
                    ] = request.user.account.favorites.favorites_items.values_list(
                        "product__id", flat=True
                    )
                    # additional['compare_list'] = [item.product.id for item in
                    #                               Compare.objects.get(account__user=request.user).items()]
                except ObjectDoesNotExist:
                    additional["favorites_list"] = None
                    additional["compare_list"] = None
            else:
                try:
                    additional["favorites_list"] = [
                        k.product.id for k in request.session["favorites"].items()
                    ]
                except KeyError:
                    additional["favorites_list"] = None
                try:
                    additional["compare_list"] = [
                        k.product.id for k in request.session["compare"].items()
                    ]
                except KeyError:
                    additional["compare_list"] = None
            # Сериализация требуемых олбъектов
            context["products"] = ""
            # if context["tile"]:
            #     context['products'] += '<div class="row">'
            #     for item in products:
            #         context['products'] += \
            #             '<div class="col-lg-4 col-sm-6 col-12">' \
            #             + item.the_product_card(additional) + '</div>'
            #     context['products'] += '</div>'
            # else:
            #     for item in products:
            #         context['products'] += item.the_product_card_wide(additional)

            context["products"] = get_template("catalog/product-cards.html").render(
                {
                    "products": products,
                    "additional": additional,
                    "tile": context["tile"],
                    "price_type": context.get("price_type", None),
                    "request": request,
                }
            )
            context["count"] = count_products
            context["word"] = format_word(count_products)
            context[
                "display_related_categories_and_filters"
            ] = obj.display_related_categories_and_filters
            return self.render_to_json_response(context, **response_kwargs)
        else:
            context["salemode"] = "salemode" in request.GET.keys()
            context["stockmode"] = "stockmode" in request.GET.keys()
            del products
            context["products"] = True
            return super().render_to_response(context, **response_kwargs)


class CardTypeView(View):
    def post(self, request, *args, **kwargs):

        card_type = request.POST.get("type", "tile")

        if card_type == "tile" or card_type == "wide":
            change = False
            card = request.session.get("card_type", "")
            if card:
                if not card == card_type:
                    request.session["card_type"] = card_type
                    change = True
            else:
                request.session["card_type"] = card_type
                change = True
            request.session.save()

            return JsonResponse({"error": False, "change": change})
        else:
            return JsonResponse({"error": True, "sss": card_type})


class BrandsList(ListView):
    model = Brand
    context_object_name = "brands"
    template_name = "catalog/brands.html"
    try:
        queryset = model.objects.filter(active=True).order_by("sort", "title")
    except ObjectDoesNotExist:
        queryset = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["english_alphabet"] = string.ascii_uppercase
        a_unicode = ord("а")
        russian_alphabet = [
            chr(letter).upper() for letter in range(a_unicode, a_unicode + 32)
        ]
        exclude_chars = ["Ъ", "Ы", "Ь"]
        [russian_alphabet.remove(char) for char in exclude_chars]
        context["russian_alphabet"] = russian_alphabet
        qs = self.queryset
        active_letters = qs.annotate(
            first_letter=Upper(Substr("title_upper", 1, 1))
        ).values_list("first_letter", flat=True)
        context["active_letters"] = active_letters
        return context

    def post(self, request, *args, **kwargs):
        post_data = request.POST.copy()
        letter = post_data.get("letter", "a")
        letter = str(letter).upper()
        qs = self.queryset
        qs = qs.filter(title_upper__startswith=letter).order_by("title", "sort")
        template = get_template("catalog/includes/brand-items.html")
        template = template.render({"brands": qs})
        return JsonResponse({"template": template})


class BrandDetail(DetailView):
    """Страница бренда"""

    obj = None
    model = Brand
    context_object_name = "brand"
    template_name = "catalog/brand.html"

    def get_context_data(self, **kwargs):
        context = super(BrandDetail, self).get_context_data(**kwargs)

        brand = context["object"]
        context["brand_cats"] = (
            Category.objects.filter(products__brand__id=brand.id)
            .order_by("parent")
            .distinct()
        )

        return context

    def get_object(self, queryset=None):
        try:
            obj = super(BrandDetail, self).get_object(queryset=queryset)
            return obj
        except ObjectDoesNotExist:
            raise Http404


class ProductDatail(DetailView):
    """Страница товара"""

    obj = None
    model = Product
    context_object_name = "product"
    template_name = "catalog/product.html"

    def get_context_data(self, **kwargs):
        context = super(ProductDatail, self).get_context_data(**kwargs)

        product = context["object"]
        category = product.category

        # Добавление текущего товара в просмотренные товары
        product.set_viewed_products(self.request)

        # Просмотренные товары
        context["viewed_products"] = product.get_viewed_products(self.request)

        similar_products = product.get_similar_items()
        context["similar_products"] = similar_products
        context["similar_count"] = similar_products.count()

        options = product.options.filter(active=True)
        context["options"] = options

        return context

    def get_object(self, queryset=None):
        try:
            obj = super(ProductDatail, self).get_object(queryset=queryset)
            return obj
        except ObjectDoesNotExist:
            raise Http404


# class ProductsJSONTemplate(
#     JSONResponseMixin, SingleObjectTemplateResponseMixin, TemplateView
# ):
#     """
#     Страница со всеми товарами. Если был Ajax запрос будет возвращен `Json`
#     страницы, иначе будет возвращен `HTML` документ.
#     """

#     template_name = "catalog/products.html"

#     def render_to_response(self, context, **response_kwargs):
#         request = self.request
#         search = request.GET.get("search", "")
#         context["search"] = search
#         # up_search = search.upper()
#         # ru, en = translate_search(search.upper())
#         filtr = None
#         category = request.GET.get("category") or ""
#         if category.isdigit():
#             category = int(category)
#         else:
#             category = None
#         context["category"] = category
#         exclude_category = _get_exclude_category()
#         if not category:
#             pr = Product.objects.exclude(category_id__in=exclude_category)
#         else:
#             print("category", category)
#             pr = Category.get_products(category=Category.objects.get(id=category))
#         # if search:
#         #     filtr = Q(search=up_search)

#         if ("salemode" in request.GET.keys()) and request.GET.get("sale"):
#             filtr = Q(old_price__gt=0) | Q(sale=True)
#         if filtr:
#             pr = pr.filter(filtr)
#         if not request.GET.get("sale"):
#             code = pr.filter(code=search)
#             if code.exists():
#                 products_visible = code
#                 products = code
#             else:
#                 products_visible = _get_products_query(
#                     search=search, products=pr, order=self.request.GET.get("sort")
#                 )
#                 products = Product.objects.filter(
#                     id__in=list(products_visible.values_list("id", flat=True))
#                 )
#         else:
#             products = pr
#             products_visible = pr
#         cat_filters = []
#         parameters_get = ""
#         filtered_groups = []
#         only_count = not bool(category)
#         pick_category = None
#         if self.request.GET.get("ajax") == "Y":
#             if category:
#                 pick_category = Category.objects.get(id=category)
#                 if pick_category.slug in ['boilery']:
#                     only_count = False
#                 else:
#                     only_count = pick_category.parent is None
#             print(category, search, only_count, pick_category)
#             context["filters"] = Product.get_filters(products, only_count=only_count, category=pick_category)
#             only_count = context["filters"].get("only_count", False)
#             products, context["active"] = Product.filter_products(products, request)
#             context["filtration_after"], filtered_groups = Product.get_after_filters(
#                 products, True
#             )
#             dir_ids = [int(x.split("_")[-1]) for x in context["active"]["directions"]]
#             cat_filters = (
#                 Category.objects.exclude(id__in=exclude_category)
#                     .filter(products__directions__id__in=dir_ids)
#                     .distinct()
#             )
#             parameters_get = "?"
#             for p in self.request.GET.items():
#                 if p[0] != "ajax":
#                     parameters_get += "&{}={}".format(p[0], p[1])

#         card_type = request.session.get("card_type", "")

#         if card_type == "tile":
#             context["tile"] = True
#         else:
#             context["tile"] = False

#         web_settings = Settings.objects.filter(language=request.LANGUAGE_CODE).first()
#         if not web_settings:
#             web_settings = Settings.objects.first()
#             if not web_settings:
#                 web_settings = Settings(language="fallback")
#         # Пагинация и кнопка показать еще
#         if self.request.GET.get("ajax") == "Y":
#             # Возвращение данных в виде Json
#             count_products = products_visible.count()
#             if count_products > 0:
#                 page = int(request.GET.get("page", 1))
#                 if int(count_products) <= int(12):
#                     # context['more_button'] = ""
#                     context["pagination"] = ""
#                 else:
#                     pagin = pagination(products_visible, page, 12)
#                     products = pagin.items
#                     context["pagination"] = get_template(
#                         "catalog/includes/pagination.html"
#                     ).render({"PAGIN": pagin})

#             # sale_category_list = Category.objects.filter(active=True) # Product.sale_filter(Product.objects.filter(active=True)).values_list('category__title', flat=True)
#             if request.GET.get("sale"):
#                 sale_products = Product.sale_filter(Product.objects.filter(active=True))
#             else:
#                 sale_products = products_visible

#             sale_category_list = (
#                 sale_products.order_by("category")
#                     .distinct("category")
#                     .values_list("category", flat=True)
#             )
#             sale_category_set = set()
#             for sale_category in sale_category_list:
#                 sale_category_set.update(
#                     Category.objects.get(id=sale_category)
#                         .get_ancestors(include_self=True)
#                         .values_list("id", flat=True)
#                 )
#             categories = request.GET.get("categories", [])
#             if categories:
#                 categories = categories.split(",")
#                 sale_category_set = Category.objects.filter(id__in=categories)
#             else:
#                 categories = sale_category_set
#             sale_category_list = Category.objects.filter(id__in=sale_category_set)
#             # Удаление лишних объектов
#             del context["view"]
#             template_filter = get_template("catalog/includes/filters.html").render(
#                 {
#                     "filters": context["filters"],
#                     "active": context["active"],
#                     "filtration_after": context["filtration_after"],
#                     "settings": web_settings,
#                     "count_products": count_products,
#                     "cat_filters": cat_filters,
#                     "parameters_get": parameters_get,
#                     "filtered_groups": filtered_groups,
#                     "sale_category_list": sale_category_list
#                     if "salemode" in request.GET.keys()
#                     else sale_category_list,
#                     "categories": categories,
#                     "in_category": only_count,
#                     "search": search,
#                     "category": category,
#                     "only_count": not (only_count and pick_category),
#                 }
#             )
#             context["template_filters"] = template_filter

#             # Сериализация требуемых объектов
#             context["products"] = ""
#             if context["tile"]:
#                 context["products"] += '<div class="row">'
#                 for item in products:
#                     context["products"] += (
#                             '<div class="col-lg-4 col-sm-6 col-12">'
#                             + item.the_product_card()
#                             + "</div>"
#                     )
#                 context["products"] += "</div>"
#             else:
#                 for item in products:
#                     context["products"] += item.the_product_card_wide()
#             return self.render_to_json_response(context, **response_kwargs)

#         del products
#         context["salemode"] = "salemode" in request.GET.keys()
#         context["products"] = True
#         return super().render_to_response(context, **response_kwargs)


class ProductsJSONTemplateDebug(
    JSONResponseMixin, SingleObjectTemplateResponseMixin, TemplateView
):
    """
    Страница со всеми товарами. Если был Ajax запрос будет возвращен `Json`
    страницы, иначе будет возвращен `HTML` документ.
    """

    template_name = "catalog/products.html"

    def render_to_response(self, context, **response_kwargs):
        request = self.request
        search = request.GET.get("search", "")
        context["search"] = search
        # up_search = search.upper()
        # ru, en = translate_search(search.upper())
        filtr = None
        category = request.GET.get("category") or ""
        if category.isdigit():
            category = int(category)
        else:
            category = None
        context["category"] = category
        exclude_category = _get_exclude_category()

        sort = request.GET.get("sort", "sort")

        categories_order = None
        if search:
            product_documents = search_elastic(search, sort_fields=[sort, "_score"])
            # считаем сколько товаров встречается в каждой категории
            categories_counter = Counter(
                doc.category_root_id for doc in product_documents
            )
            when_list = []
            for pk, count in categories_counter.items():
                # добавляем отрицательное количество(тогда категория с наибольшим количеством будет вначале)
                when_list.append(When(pk=pk, then=-count))
                # добавляем дочерним категориям 0.5 чтобы сохранить вложенность
                when_list.append(When(parent__id=pk, then=-count + 0.5))
            if when_list:
                categories_order = Case(*when_list, output_field=CharField())
            pr = product_documents.to_queryset()
        else:
            pr = Product.objects.filter(active=True).order_by(sort)
        if not category:
            pr.exclude(category_id__in=exclude_category)
        else:
            print("category", category)
            if isinstance(category, int):
                category = Category.objects.get(id=category)
            pr = pr.filter(**Category.get_products_query(category))
        # if request.GET.get("sort") and request.GET['sort'] != 'sort':
        #     pr = pr.order_by(*request.GET["sort"].split(","))

        if ("salemode" in request.GET.keys()) and request.GET.get("sale"):
            filtr = Q(old_price__gt=0) | Q(sale=True)
        else:
            print("|||||||")
            print("|||||||")
            print("|||||||")
            print("|||||||")
        if filtr:
            pr = pr.filter(filtr)
        if not request.GET.get("sale"):
            code = Product.objects.filter(active=True)
            if search:
                code = code.filter(code__iexact=search)
            if code.exists() and search:
                products_visible = code
                products = pr
            else:
                products_visible = pr
                products = pr
                # products_visible = elastic_search(
                #     phrase=phrase, products=pr, order=self.request.GET.get("sort")
                # )
                # products = Product.objects.filter(
                #     id__in=list(products_visible.values_list("id", flat=True))
                # )
        else:
            products = pr
            products_visible = pr
        cat_filters = []
        parameters_get = ""
        filtered_groups = []
        only_count = False
        if self.request.GET.get("ajax") == "Y":
            curcat = self.request.GET.get("category", 0)
            if curcat == "None":
                only_count = True
            else:
                only_count = not bool(self.request.GET.get("category", 0))
            # get_filter_products = Product.objects.filter(active=True)
            # get_filter_products = get_filter_products.filter(
            #     category=category
            # )
            context["filters"] = Product.get_filters(
                products,
                only_count=only_count,
                request=request,
            )
            only_count = context["filters"].get("only_count", False)
            products, context["active"] = Product.filter_products(
                products, request, keep_order=True
            )
            print(products, context["filters"])
            if request.user.is_authenticated:
                if not request.user.account.is_price_type_default:
                    products = products.filter(
                        prices__type=request.user.account.price_type
                    )
            context["filtration_after"], filtered_groups = Product.get_after_filters(
                products, True
            )
            dir_ids = [int(x.split("_")[-1]) for x in context["active"]["directions"]]
            cat_filters = (
                Category.objects.exclude(id__in=exclude_category)
                .filter(products__directions__id__in=dir_ids)
                .distinct()
            )
            parameters_get = "?"
            for p in self.request.GET.items():
                if p[0] != "ajax":
                    parameters_get += "&{}={}".format(p[0], p[1])

        card_type = request.session.get("card_type", "")

        if card_type == "tile":
            context["tile"] = True
        else:
            context["tile"] = False

        web_settings = Settings.objects.filter(language=request.LANGUAGE_CODE).first()
        if not web_settings:
            web_settings = Settings.objects.first()
            if not web_settings:
                web_settings = Settings(language="fallback")
        # Пагинация и кнопка показать еще
        if self.request.GET.get("ajax") == "Y":
            count_products = products.count()
            # Возвращение данных в виде Json
            if count_products > 0:
                page = int(request.GET.get("page", 1))
                if count_products <= 12:
                    context["pagination"] = None
                else:
                    pagin = pagination(products, page, 12)
                    products = pagin.items
                    context["pagination"] = get_template(
                        "catalog/includes/pagination.html"
                    ).render({"PAGIN": pagin})
            else:
                count_products = 0

            if request.GET.get("sale"):
                sale_products = Product.objects.filter(
                    active=True, sale=True, count__gt=0
                )
            else:
                sale_products = products_visible
            sale_category_list = (
                sale_products.exclude(category=None)
                .exclude(category__display_in_categories=False)
                .order_by("category")
                .distinct("category")
                .values_list("category", flat=True)
            )
            sale_category_set = set(sale_category_list.values_list("id", flat=True))
            for sale_category in sale_category_list:
                sale_category_set.update(
                    Category.objects.get(id=sale_category)
                    .get_ancestors(include_self=True)
                    .values_list("id", flat=True)
                )
            categories = request.GET.get("categories", [])
            if categories:
                categories = categories.split(",")
            else:
                categories = sale_category_set
            sale_category_list = Category.objects.filter(
                id__in=sale_category_set,
                level__lt=2,
                active=True,
            )
            print("--", categories_order)
            if categories_order:
                sale_category_list = sale_category_list.order_by(categories_order)
            print(sale_category_list)
            # Удаление лишних объектов
            del context["view"]
            template_filter = get_template("catalog/includes/filters.html").render(
                {
                    "filters": context["filters"],
                    "active": context["active"],
                    "filtration_after": context["filtration_after"],
                    "settings": web_settings,
                    "count_products": count_products,
                    "cat_filters": cat_filters,
                    "parameters_get": parameters_get,
                    "filtered_groups": filtered_groups,
                    "sale_category_list": sale_category_list,
                    "categories": categories,
                    "in_category": False,
                    "search": search,
                    "category": category,
                    "only_count": only_count,
                }
            )
            context["template_filters"] = template_filter

            # Сериализация требуемых объектов
            context["products"] = ""
            if context["tile"]:
                context["products"] += '<div class="row">'
                for item in products:
                    context["products"] += (
                        '<div class="col-lg-4 col-sm-6 col-12">'
                        + item.the_product_card(request=request)
                        + "</div>"
                    )
                context["products"] += "</div>"
            else:
                for item in products:
                    context["products"] += item.the_product_card_wide(request=request)
            return self.render_to_json_response(context, **response_kwargs)

        del products
        context["salemode"] = "salemode" in request.GET.keys()
        context["products"] = True
        return super().render_to_response(context, **response_kwargs)


def _is_ru(word: str) -> bool:
    return word.upper() in list("ёйцукенгшщзхъфывапролджэячсмитьбю".upper())


def translate_search(search: str):
    """Принимает фразу и возвращает ее на русской и английский раскладке"""
    alph_en = list("`qwertyuiop[]asdfghjkl;'zxcvbnm,.".upper())
    alph_ru = list("ёйцукенгшщзхъфывапролджэячсмитьбю".upper())
    en = ""
    ru = ""
    for word in list(search.upper()):
        if word in alph_ru or word in alph_en:
            if _is_ru(word):
                ru += word
                en += alph_en[alph_ru.index(word)]
            else:
                ru += alph_ru[alph_en.index(word)]
                en += word
        else:
            ru += word
            en += word
    return ru, en


def search_query(search: str, products=None) -> list:
    if products is None:
        exclude_category = _get_exclude_category()
        products = Product.objects.exclude(category_id__in=exclude_category).filter(
            active=True
        )
    if search:
        products = _get_products_query(products=products, search=search)
    return list(products.values_list("id", flat=True))


# from apps.catalog.views import *
# search_query('Манометр ТМ321')


def test():
    a = _get_exclude_category()
    print(a)
    return a


def _get_exclude_category():
    cat = Category.objects.only("id", "tree_id", "level", "lft", "rght", "active")
    exclude_category = []
    # Получение неактивных категорий
    for c in cat.filter(active=False).iterator():
        # Если категория уже в списке исключенных пропустить
        if c.id in exclude_category:
            continue
        # Если категория неактивна добавить в список неактивных ее и всех ее детей
        exclude_category += list(
            c.get_descendants(include_self=True).values_list("id", flat=True)
        )
    disabled_category = Category.objects.filter(
        unloading_id="82f466e6-e06e-11dd-97c1-0016e65f1671"
    ).first()
    if not disabled_category:
        return exclude_category
    exclude_category += disabled_category.get_descendants(
        include_self=True
    ).values_list("id", flat=True)
    return exclude_category


def _get_products_query(search, products=None, order=None):
    """Собираем запрос для продуктов"""
    pretext = (
        "в,о,с,у,к,от,до,для,на,по,со,из,над,под,при,про"
        "b,j,c,e,r,jn,lj,lkz,yf,gj,cj.bp,yfl,gjl,ghb,ghj".split(",")
    )
    search = " ".join(
        [word for word in search.split(" ") if word.lower() not in pretext]
    )
    ru, en = translate_search(
        search=search
    )  # Получаем русскую и английскую версию слова
    search_vector = (
        SearchVector("title", weight="B")
        + SearchVector("title_upper", weight="A")
        + SearchVector("description_upper", weight="C")
    )
    if products is None:
        products = Product.objects.filter(active=True)
    # annotate = {
    #     'search': search_vector,
    #     'similarity': TrigramSimilarity('title', search) + TrigramSimilarity('title', ru) + TrigramSimilarity('title',
    #                                                                                                           en),
    # }
    ru = ru.lower()
    en = en.lower()
    search = search.lower()
    if ru == search:
        sq = SearchQuery(search) | SearchQuery(en)
        similarity = Greatest(
            TrigramSimilarity("title", search)
            + TrigramSimilarity("title_upper", search),
            TrigramSimilarity("title", en) + TrigramSimilarity("title_upper", en),
        )
    elif en == search:
        sq = SearchQuery(search) | SearchQuery(ru)
        similarity = Greatest(
            TrigramSimilarity("title", search)
            + TrigramSimilarity("title_upper", search),
            TrigramSimilarity("title", ru) + TrigramSimilarity("title_upper", ru),
        )
    else:
        sq = SearchQuery(search) | SearchQuery(ru) | SearchQuery(en)
        similarity = Greatest(
            TrigramSimilarity("title", search)
            + TrigramSimilarity("title_upper", search),
            TrigramSimilarity("title", en) + TrigramSimilarity("title_upper", en),
            TrigramSimilarity("title", ru) + TrigramSimilarity("title_upper", ru),
        )
    annotate = {
        "rank": SearchRank(search_vector, sq),
        "similarity": similarity,
    }
    filter_q = Q(similarity__gte=0.07, rank__gte=0)
    only = ["title_upper", "description_upper", "code", "title", "thumbnail"]
    if not order or order == "sort":
        order = "-rank,-similarity"
    response = (
        products.annotate(**annotate)
        .filter(filter_q)
        .order_by(*order.split(","))
        .only(*only)
    )
    return response


def _get_category_query(categories, lang: str, n=10):
    """Собираем запрос для категорий"""
    if not lang.strip():
        return categories.objects.none()
    search_vector = SearchVector("title")
    annotate = {"search": search_vector, "similarity": TrigramSimilarity("title", lang)}
    filter_q = Q(similarity__gt=0.1) | Q(search=lang)
    categories = (
        categories.annotate(**annotate)
        .filter(filter_q, level__lt=2)
        .order_by("-similarity", "level")[:n]
    )
    return categories


# Поиск пгрес
# class SearchView(View):
#     """Обработчик запроса на поиск товаров"""

#     def post(self, request):
#         post_data = request.POST
#         search = post_data["search"]
#         exclude_category = _get_exclude_category()
#         ru, en = translate_search(search.upper())
#         code = Product.objects.exclude(category_id__in=exclude_category).filter(
#             code__icontains=search
#         )[:3]
#         products, categories = [], []
#         if not code:
#             products = _get_products_query(
#                 products=Product.objects.exclude(category_id__in=exclude_category),
#                 search=search,
#             )[:10]
#             categories = Category.objects.exclude(id__in=exclude_category)
#             categories = _get_category_query(categories, ru) or _get_category_query(
#                 categories, en
#             )

#         # vector = F('search_vector')
#         # products_without_brand = Product.objects.annotate(
#         #         search=vector
#         # ).filter(
#         #     Q(active=True)
#         #     & Q(brand__isnull=True)
#         #     & Q(Q(search__icontains=up_search) | Q(brand__title_upper=up_search))
#         # ) #.query

#         # vector = vector._combine(F('brand__search_vector'), '||', False) # без комментариев
#         # products_with_brand = Product.objects.annotate(
#         #         search=vector
#         # ).filter(
#         #     Q(active=True)
#         #     & Q(brand__isnull=False)
#         #     & Q(Q(search__icontains=up_search) | Q(brand__title_upper=up_search))
#         # )

#         # products = (products_without_brand | products_with_brand)[:10]

#         # print(products)

#         # categorys = Category.objects.exclude(id__in=exclude_category).filter(title__icontains=search)[:10]

#         # collections = Product.objects.filter(type_obj = "collection").filter(
#         # Q(Q(title__icontains=search) | Q(code__icontains=search)))[:10]

#         # Если по запросу нет товаров или услуг, то возвращаем сообщение о том
#         # что по данному запросу ничего не найдено
#         if not products and not categories and not code:
#             return JsonResponse({"error": True, "message": "Ничего не найдено"})

#         template = get_template("catalog/includes/search-result.html").render(
#             {"products": products, "code": code, "categorys": categories}
#         )

#         # for item in products:
#         #     response += '<a class="search-form__dropdown-item" \
#         #     href="{0}">{1}</a>'.format(
#         #         item.get_absolute_url(), item.title)

#         return JsonResponse({"template": template})


# Поиск эластик
class SearchView(View):
    """Обработчик запроса на поиск товаров"""

    def post(self, request):
        post_data = request.POST
        search = post_data["search"]
        exclude_category = _get_exclude_category()
        ru, en = translate_search(search.upper())
        code = Product.objects.exclude(category_id__in=exclude_category).filter(
            code__icontains=search
        )[:3]
        products, categories = [], []
        if not code:
            # так как мы не фильтруем в эластике на активность категорий,
            #  то берем 15 товаров и потом уже производим фильтрацию
            products = list(
                search_elastic(search, 15)
                .to_queryset()
                .exclude(category_id__in=exclude_category)
            )[:10]
            categories = Category.objects.exclude(id__in=exclude_category)
            categories = _get_category_query(categories, ru) or _get_category_query(
                categories, en
            )

        # Если по запросу нет товаров или услуг, то возвращаем сообщение о том
        # что по данному запросу ничего не найдено
        if not products and not categories and not code:
            return JsonResponse({"error": True, "message": "Ничего не найдено"})

        template = get_template("catalog/includes/search-result.html").render(
            {"products": products, "code": code, "categorys": categories}
        )

        return JsonResponse({"template": template})
