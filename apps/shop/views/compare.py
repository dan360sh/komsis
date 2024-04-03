
from apps.catalog.models import (Attribute, AttributesGroup, Category,
                                 NumAttribute, Product)
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import get_template
from django.views.generic import TemplateView, View

from ..models import Compare, CompareItem, UnauthCompare, UnauthCompareItem


class CompareView(TemplateView):
    """Представление странцы избранных товаров магазина"""

    template_name = 'shop/compare.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # получаем товары для сравнения
        if self.request.user.is_authenticated:
            try:
                compare = Compare.objects.get(
                    account__user=self.request.user)
            except ObjectDoesNotExist:
                compare = []
        else:
            try:
                compare = self.request.session['compare']
            except KeyError:
                compare = []
        # формируем список из товаров
        if compare:
            products = [p.product for p in compare.items()]
        else:
            products = []
        # получаем категории товаров
        categories = Category.objects.filter(products__in=products).distinct()
        # получаем ид требуемой категории
        cat_id = self.request.GET.get("cat", 0)
        try:
            category = Category.objects.get(id=int(cat_id))
        except:
            category = categories.first()
        # товары нужной нам категории
        # products = products.filter(category=category)
        new_products = [p for p in products if p.category == category]
        products = new_products
        # получение атрибутов товаров
        context['attributes'] = AttributesGroup.objects.filter(
            Q(attributes__product__in=products) |
            Q(num_attributes__product__in=products)).distinct()

        attrs = list(Attribute.objects.filter(product__in=products))
        num_attrs = list(NumAttribute.objects.filter(product__in=products))
        context['attrs_prods'] = attrs + num_attrs
        context['compare_products'] = products
        context['categories_comare'] = categories
        context['category'] = category
        return context


class AddCompareView(View):
    """Представление добавления товара в избранные"""

    def post(self, request):
        post_data = request.POST
        product = Product.objects.get(id=int(post_data['product']))

        # Добавление в избранные
        if request.user.is_authenticated:
            compare = self.update_auth_compare(request, product)
        else:
            compare = self.update_unauth_compare(request, product)

        return JsonResponse({'count': compare.count()})

    def update_auth_compare(self, request, product):
        """Добавление товара в избранные товары авторизованного пользователя.

        Arguments:
            request {object} -- Запрос на сервер
            product {Product} -- Товар

        Returns:
            Compare -- Экземпляр модели избранных товаров авторизванного
            пользователя
        """

        compare = Compare.objects.get(account__user=self.request.user)
        compare_item, created = CompareItem.objects.get_or_create(
            compare=compare, product=product)
        if not created:
            compare_item.delete()
        return compare

    def update_unauth_compare(self, request, product):
        """Добаление товара в избранные товары не авторизованного
        пользователя(избранные добавляется в сессию).

        Arguments:
            request {object} -- Запрос на сервер
            product {Product} -- Товар

        Returns:
            UnauthCompare -- Избранные товары не авторизванного пользователя
        """

        compare = request.session.get('compare', None)
        if compare:
            found_item = False
            for item in compare.compare_items:
                if item.product == product:
                    found_item = True
            if not found_item:
                compare.compare_items.append(
                    UnauthCompareItem(product=product))
        else:
            compare = UnauthCompare(
                compare_items=[UnauthCompareItem(product=product)])
        request.session['compare'] = compare
        request.session.save()
        return compare


class DeleteCompareView(View):
    """Представление удаления товара из избранных"""

    def post(self, request):
        post_data = request.POST
        product = Product.objects.get(id=int(post_data['product']))

        # Добавление в избранные
        if request.user.is_authenticated:
            compare = self.update_auth_compare(request, product)
        else:
            compare = self.update_unauth_compare(request, product)

        restore = get_template(
            template_name='shop/includes/compare-restore.html').render(
                {'product': product})

        return JsonResponse({'count': compare.count(), 'restore': restore})

    def update_auth_compare(self, request, product):
        compare = Compare.objects.get(account__user=request.user)
        CompareItem.objects.get(
            compare=compare, product=product).delete()
        return compare

    def update_unauth_compare(self, request, product):
        compare = request.session.get('compare', None)
        for key, item in enumerate(compare.compare_items):
            if item.product == product:
                del compare.compare_items[key]
        request.session['compare'] = compare
        request.session.save()
        return compare


class RestoreCompareView(View):
    """Представление восстановления товара в избранных"""

    def post(self, request):
        post_data = request.POST
        product = Product.objects.get(id=int(post_data['product']))

        # Добавление в избранные
        if request.user.is_authenticated:
            compare = self.update_auth_compare(request, product)
        else:
            compare = self.update_unauth_compare(request, product)

        return JsonResponse({'count': compare.count()})

    def update_auth_compare(self, request, product):
        compare = Compare.objects.get(account__user=request.user)
        CompareItem.objects.update_or_create(
            compare=compare, product=product)
        return compare

    def update_unauth_compare(self, request, product):
        compare = request.session.get('compare', None)
        compare.compare_items.append(UnauthCompareItem(product=product))
        request.session['compare'] = compare
        request.session.save()
        return compare
