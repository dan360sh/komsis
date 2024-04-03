import json
import re

from apps.catalog.models import Color, Option, Product
from django.http import JsonResponse
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.encoding import repercent_broken_unicode
from django.views.generic import TemplateView, View

from ..models import Cart, CartItem, UnauthCart, UnauthCartItem


class CartTemplate(TemplateView):
    template_name = 'shop/cart.html'


class CartAddView(View):
    """
    Обработчик добавления товаров и опций в корзину.
    """

    def post(self, request):
        post_data = request.POST
        product = Product.objects.get(id=int(post_data['product-id']))
        count = int(post_data.get('product-count', 1))
        colors = product.colors.all()

        try:
            color = Color.objects.get(id=int(post_data['product-color']))
        except KeyError:
            color = None
            if colors:
                return JsonResponse({
                    'errors': True, 'message': 'Выберите цвет'})

        try:
            option = Option.objects.get(id=int(post_data['product-option']))
        except KeyError:
            option = None
            if option:
                return JsonResponse({
                    'errors': True, 'message': 'Выберите опцию'})

        if post_data.get('products', False):
            products = json.loads(post_data['products'])
            for item in products:
                option = Option.objects.get(id=int(item['option']))
                if request.user.is_authenticated:
                    cart = self.create_auth_cart(
                        request, product, color, option, int(item["count"]))
                else:
                    cart = self.create_unauth_cart(
                        request, product, color, option, int(item["count"]))
            return JsonResponse({
                'count': cart.count(),
                'dropdown': render_dropdown(cart, request),
                'ecommerce-product': {"id": str(product.id), "name": str(product.title), "price": str(option.price),
                                      "category": str(product.category.title),
                                      "quantity": count}
            })

        if request.user.is_authenticated:
            cart = self.create_auth_cart(
                request, product, color, option, count)
        else:
            cart = self.create_unauth_cart(
                request, product, color, option, count)
        p = product
        return JsonResponse({
            'count': cart.count(),
            'dropdown': render_dropdown(cart, request),
            'ecommerce-product': {"id": str(p.id), "name": str(p.title), "price": str(p.price),
                                  "category": str(p.category.title), "quantity": count}
        })

    def create_auth_cart(self, request, product, color, option, count):
        """Создание корзины товаров авторизованного пользователя.

        Arguments:
            request {DjangoRequest} -- Запрос на сервер
            product {Product} -- Экземпляр товара
            color {Color} -- Экземпляр опции цвета товара
            count {int} -- Количество товаров

        Returns:
            Cart -- Корзина товаров
        """

        cart = Cart.objects.get(account__user=request.user)
        account = request.user.account
        fields = {'count': count}
        cart_item, created = CartItem.objects.select_related("product").get_or_create(
            cart=cart, product=product, color=color, option=option, defaults=fields)
        if not created:
            if (count + cart_item.count) >= cart_item.product.count:
                if product.is_able_to_overflow_count:
                    # Добавляем возможность каждому пользователю
                    # заказывать товары сверх остатка
                    cart_item.count = count
                else:
                    cart_item.count = cart_item.product.count
            else:
                cart_item.count += count
            cart_item.save()
        return cart

    def create_unauth_cart(self, request, product, color, option, count):
        """Создание корзины товаров неавторизованного пользователя.

        Arguments:
            request {DjangoRequest} -- Запрос на сервер
            product {Product} -- Экземпляр товара
            color {Color} -- Экземпляр опции цвета товара
            count {int} -- Количество товаров

        Returns:
            UnauthCart -- Корзина товаров
        """

        cart = request.session.get('cart', None)
        if cart:
            if cart.count():
                found_item = False
                for key, item in enumerate(cart.cart_items):
                    if item.product == product and item.color == color and item.option == option:
                        # Если был найден переданный товар
                        found_item = True
                        if (item.count + count) >= item.product.count:
                            # если кол-во товаров в корзине будет первышать
                            # остаток товаров на складе
                            if product.is_able_to_overflow_count:
                                # если у товара есть возможность превышать остаток
                                cart.cart_items[key].count = count
                            else:
                                # если нет, просто делаем кол-во товара в корзине равным
                                # остатку товара
                                cart.cart_items[key].count = item.product.count
                        else:
                            cart.cart_items[key].count = item.count + count
                if not found_item:
                    cart.add(UnauthCartItem(
                        product=product, color=color, option=option, count=count))
            else:
                cart.cart_items = [UnauthCartItem(
                    product=product, color=color, option=option, count=count)]
        else:
            cart = UnauthCart(cart_items=[UnauthCartItem(
                product=product, color=color, option=option, count=count)])
        request.session['cart'] = cart
        request.session.save()
        return cart


class CartUpdateView(View):
    """Обработчик обновление количества товаров и их суммы в корзине.

    Arguments:
        View {object} -- Базовый класс представлений Django.

    Returns:
        dict -- Возвращаяет данные корзины в виде json.
    """

    def post(self, request):
        post_data = request.POST
        count = int(post_data['product-count'])

        product = Product.objects.get(id=post_data['product-id'])
        try:
            color = Color.objects.get(id=int(post_data['product-color']))
        except KeyError:
            color = None
        try:
            option = Option.objects.get(id=int(post_data['product-option']))
        except KeyError:
            option = None
        if request.user.is_authenticated:
            cart, cart_item = self.update_auth_cart_item(
                request, product, color, option, count)
        else:
            cart, cart_item = self.update_unauth_cart_item(
                request, product, color, option, count)
        p = product
        user = request.user
        account = user.account if user.is_authenticated else None
        response_price = cart_item.count_total_by_account(account)
        response_total = cart.count_total_by_account(account)
        is_overflowed = cart_item.is_count_overflowed
        json_response = {
            'product_id': cart_item.product.id if not cart_item.option else cart_item.option.id,
            'item_count': cart_item.count,
            'count': cart.count(),
            'price': round(response_price, 2),
            'total': round(response_total, 2),
            'is_overflowed': is_overflowed,
            'dropdown': render_dropdown(cart, request),
            'ecommerce-product': {"id": str(p.id), "name": str(p.title),
                                  "price": str(option.price) if option else str(p.price),
                                  "category": str(p.category.title), "quantity": str(count)}
        }
        return JsonResponse(json_response)

    def update_auth_cart_item(self, request, product, color, option, count):
        """Обновление элемента в корзине авторизованного пользователя.

        Arguments:
            request {object} -- Запрос на сервер
            product {Product} -- Товар
            color {Color} -- Опция цвета
            count {int} -- Количесто товаров

        Returns:
            (Cart, CartItem) -- Корзина товаров и измененный
            элемент корзины
        """

        cart = Cart.objects.filter(account__user=request.user).first()
        cart_item = CartItem.objects.get(
            cart=cart, product=product, color=color, option=option)

        account = request.user.account
        if count > cart_item.product.get_total_count():
            if product.is_able_to_overflow_count:
                cart_item.count = count
            else:
                cart_item.count = cart_item.product.get_total_count()
        else:
            cart_item.count = count
        cart_item.save()
        return cart, cart_item

    def update_unauth_cart_item(self, request, product, color, option, count):
        """Обновление элемента в корзине неавторизованного пользователя.

        Arguments:
            request {object} -- Запрос на сервер
            product {Product} -- Товар
            color {Color} -- Опция цвета
            count {int} -- Количесто товаров

        Returns:
            (UnauthCart, UnauthCartItem) -- Корзина товаров и измененный
            элемент корзины
        """

        cart = request.session['cart']
        for key, item in enumerate(cart.cart_items):
            if item.product == product and item.color == color and item.option == option:
                if count > cart.cart_items[key].product.count:
                    if cart.cart_items[key].product.is_able_to_overflow_count:
                        cart.cart_items[key].count = count
                    else:
                        cart.cart_items[key].count = cart.cart_items[key].product.count
                else:
                    cart.cart_items[key].count = count
                cart_item = cart.cart_items[key]
        request.session['cart'] = cart
        request.session.save()
        return cart, cart_item


class CartDeleteView(View):

    def post(self, request):
        post_data = request.POST
        product = Product.objects.get(id=post_data['product-id'])
        try:
            color = Color.objects.get(id=int(post_data['product-color']))
        except KeyError:
            color = None
        try:
            option = Option.objects.get(id=int(post_data['product-option']))
        except KeyError:
            option = None

        if request.user.is_authenticated:
            cart = self.delete_auth_cart_item(request, product, color, option)
        else:
            cart = self.delete_unauth_cart_item(
                request, product, color, option)
        user = request.user
        cart_total_price = cart.count_total_by_account(
            user.account) if user.is_authenticated else cart.total()
        p = product
        response = {'count': cart.count(),
                    'product_id': product.id,
                    'redirect': reverse_lazy("cart") if round(cart_total_price, 2) < 1 else None,
                    'total': round(cart_total_price, 2),
                    'dropdown': render_dropdown(cart, request),
                    'ecommerce-product': {"id": str(p.id), "name": str(p.title), "price": str(p.price),
                                          "category": str(p.category.title), "quantity": 1}
                    }

        if response['count'] < 1:
            response['empty'] = get_template(
                template_name='shop/includes/cart-empty.html').render()

        return JsonResponse(response)

    def delete_auth_cart_item(self, request, product, color, option):
        """Удаление элемента из корзины авторизованного пользователя

        Arguments:
            request {object} -- Запрос на сервер
            product {Product} -- Товар
            color {Color} -- Опция цвета

        Returns:
            (Cart, CartItem) -- Корзина товаров
        """

        cart = Cart.objects.get(account__user=request.user)
        CartItem.objects.get(
            cart=cart, product=product, color=color, option=option).delete()
        return cart

    def delete_unauth_cart_item(self, request, product, color, option):
        """Удаление элемента из корзины неавторизованного пользователя

        Arguments:
            request {object} -- Запрос на сервер
            product {Product} -- Товар
            color {Color} -- Опция цвета

        Returns:
            (Cart, CartItem) -- Корзина товаров
        """

        cart = request.session['cart']
        for key, item in enumerate(cart.cart_items):
            if item.product == product and item.color == color and item.option == option:
                cart.cart_items[key].product = False
                """cart.cart_items[key].option = False
                cart.cart_items[key].color = False"""
        request.session['cart'] = cart
        request.session.save()
        return cart


def render_dropdown(cart, request):
    """Рендер выпадающее меню на основе корзины товаров.

    Arguments:
        cart {Cart|UnauthCart} -- Корзина товаров

        request {object} -- Запрос на сервер

    Returns:
        str -- HTML рендер в виде строки
    """

    return get_template(template_name='shop/includes/cart-dropdown.html') \
        .render({'add_product': True, 'cart': cart, 'request': request})
