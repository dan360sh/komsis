import json
import os
import re

import requests
from apps.account.models import Account
from apps.catalog.models import ProductStorage
from apps.configuration.models import Settings, TypeShipping
from apps.configuration.utils import BankPayment, Validator
from apps.configuration.utils.bank import BankResponseKeyError
from apps.configuration.utils.send_emails import send_order_emails
from apps.feedback.models import Email
from apps.feedback.utils import template_email_message
from apps.shop.utils import (AuthOrderCreateStrategy,
                             UnauthOrderCreateStrategy, get_discount_strategy)
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.template.loader import get_template
from django.utils.text import slugify
from django.views import View
from django.views.generic import TemplateView, View

from ..models import Cart, Order

GEOCODE_URL = "https://geocode-maps.yandex.ru/1.x/"


class OrderView(TemplateView):
    context_object_name = 'order'
    template_name = 'shop/order.html'

    def post(self, request, *args, **kwargs):
        cart = self.get_cart(request)
        post_data = request.POST.copy()
        discount = post_data.get('discount', None)

        if not discount:
            raise ValueError("Ключ discount отсутствует в теле запроса")

        if not request.user.is_authenticated:
            raise AssertionError("Пользователь должен быть авторизирован")

        discount_system_strategy = get_discount_strategy(discount)
        strategy = discount_system_strategy(post_data, request, cart)
        strategy.execute()
        return JsonResponse(strategy.json_response)

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        request = self.request
        if self.request.user.is_authenticated:
            self.cart = Cart.objects.get(account__user=self.request.user)
        else:
            self.cart = self.request.session.get('cart', None)
        total = self.cart.count_total_by_account(
            request.user.account) if request.user.is_authenticated else self.cart.total()
        context['types_shipping'] = TypeShipping.objects.filter(
            is_active=True).all()
        context['excluded_shippings'] = TypeShipping.objects.filter(
            is_active=True, display_motivational=True)
        context['shops'] = Settings.get_settings().get_addresses()
        context['storages'] = ProductStorage.objects.all()

        restored_order_id = request.GET.get('order_id', None)
        if restored_order_id is not None:
            saved_order = Order.objects.get(id=restored_order_id)
            if saved_order.account == self.request.user.account:
                context['saved_order'] = saved_order

        user = self.request.user
        if user.is_authenticated:
            context['account'] = Account.objects.get(user=user)
        return context

    def get_cart(self, request):
        """Получить корзину товаров

        Arguments:
            request {object} -- Запрос на сервер
        """

        try:
            if request.user.is_authenticated:
                try:
                    return Cart.objects.get(account__user=request.user)
                except ObjectDoesNotExist:
                    raise 'Корзина не существует'
            return request.session['cart']
        except KeyError:
            raise 'Корзина не существует'


class AvailableView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.cart = Cart.objects.get(account__user=self.request.user)
        else:
            self.cart = request.session.get('cart', None)

        store_id = request.GET.get('store')
        message = self.available_problem(store_id) or None
        MANAGER_MESSAGE = "После оформления заявки на сайте мы свяжемся " + \
            "с вами. Уточним цены на интересующие товары, рассчитаем сроки " + \
            "и стоимость доставки."
        return JsonResponse({
            'products': message,
            'manager_message': MANAGER_MESSAGE
        })

    def available_problem(self, store_id):
        available_list = []
        storage_pattern = 'Склад: {} Остаток: {:g}'
        for item in self.cart.items():
            try:
                current_storage = item.product.storages.get(
                    storage_id=store_id)
            except ObjectDoesNotExist:
                current_storage = None
            if current_storage.count >= item.count:
                continue
            available_product = {
                'title': item.product.title,
                'count': item.count,
                'id': item.product.pk,
                'storages': [],
                'current_price_message': f"Цена действительна на остаток: {item.count}",
            }
            available_product['storages'].append(
                storage_pattern.format(
                    current_storage.storage,
                    current_storage.count)
            )
            # current_message = ''
            delta = item.count - current_storage.count
            another_storages = item.product.storages.exclude(
                pk=current_storage.pk).order_by('-count')
            for storage in another_storages:
                if storage.count >= delta:
                    available_product['storages'].append(
                        storage_pattern.format(storage.storage, delta))
                    break
                else:
                    available_product['storages'].append(
                        storage_pattern.format(storage.storage, storage.count))
                    delta -= storage.count
                    # message = ''.format(item.product, delta)
            available_list.append(available_product)

        return available_list


class CalculateShippingView(View):

    def get(self, request):
        type_shipping = TypeShipping.objects.get(id=request.GET.get('id_ts'))
        coord_x = request.GET.get("coord_x_delivery", "")
        coord_y = request.GET.get("coord_y_delivery", "")
        coords = coord_y + "," + coord_x
        shipping_range = float(request.GET.get("lenght", "0")) / 1000
        response = requests.get(GEOCODE_URL, params={
            'geocode': coords, 'format': 'json'})
        response = json.loads(response.text)

        def if_free():
            for obj in response['response']['GeoObjectCollection'][
                    'featureMember']:
                if obj['GeoObject']['name'] in type_shipping.get_cities_free():
                    return True
            return False

        # def if_free():
        #	 for obj in response['response']['GeoObjectCollection'][
        #			 'featureMember']:
        #		 for component in response['response']['GeoObjectCollection'][
        #			 'featureMember']['GeoObject']['metaDataProperty'][
        #				 'GeocoderMetaData']['Address']['Components']:
        #			 if component['name'] in type_shipping.get_cities_free():
        #				 return True
        #	 return False

        if type_shipping.calculation == 'price_out':
            shipping_price = "Уточняйте у хз кого"
        elif type_shipping.calculation == 'price_km':
            if if_free():
                shipping_price = "Бесплатно"
            else:
                print(shipping_range)
                print(type_shipping.price_km)
                shipping_price = "{}".format(
                    shipping_range * type_shipping.price_km)
        elif type_shipping.calculation == 'price_fix':
            if if_free():
                shipping_price = "Бесплатно"
            else:
                shipping_price = "{}".format(type_shipping.price_fix)
        else:
            shipping_price = "Уточняйте у оператора"
        shipping_price = round(float(shipping_price), 2)
        return JsonResponse({'shippingPrice': shipping_price})

    # def get_sum_order_and_delivery_price(request):
    #	 coord_x = request.GET.get("coord_x_delivery", "")
    #	 coord_y = request.GET.get("coord_y_delivery", "")
    #	 coords = coord_y + "," + coord_x
    #	 length = request.GET.get("length", "")
    #	 if not coord_x or not coord_y or not length:
    #		 return utils.JsonResponse.response(error=1, message="No full data")
    #	 sum_shipping = TypeShipping.get_price_shipping_by_coords(
    #		 coords, float(length), sum_order)
    #	 sum_order += sum_shipping
    #	 if sum_shipping == 0:
    #		 sum_shipping = "Бесплатно"
    #	 else:
    #		 sum_shipping = utils.money_format(sum_shipping)
    #	 return utils.JsonResponse.response(sum_shipping=sum_shipping)

    # def get_price_shipping_by_coords(coords, length, sum_order):
    #	 length = length/1000
    #	 sum_shipping = del_info.get_price_in_city()
    #	 if not TypeShipping.is_free_city(coords):
    #		 sum_shipping += length * BorderPrice.get_price_by_km(length)
    #	 if sum_order >= del_info.get_price_order_border():
    #		 sum_shipping -= del_info.get_price_in_city()
    #	 return round(sum_shipping)


def phone_validator(phone):
    LENGTH = 11
    FIRST_NUMS = (7, 8)
    clear_phone = re.sub('[^\d]', '', phone)
    if len(clear_phone) != LENGTH:
        return False
    elif int(clear_phone[0]) not in FIRST_NUMS:
        return False
    return True


class OrderCreate(View):
    """Представление оформелинея заказа на товары."""

    def post(self, request):
        # TODO: Валидаторы
        post_data = request.POST.copy()
        files = request.FILES
        error_list = {}
        data = {}
        cart = self.get_cart(request)
        cart_total = cart.total()
        phone = post_data.get('phone', '')
        phones_number = [v for v in phone if v.isdigit()]
        if post_data['name'] == '':
            error_list['name'] = 'Укажите имя'
        if post_data['surname'] == '':
            error_list['surname'] = 'Укажите фамилию'
        if not phone or len(phones_number) < 11:
            error_list['phone'] = 'Укажите телефон'
        if post_data.get('email', '') == '' or \
                not re.match(r"[^@]+@[^@]+\.[^@]+", post_data.get('email', '')):
            error_list['email'] = 'Укажите email'
        shipping_text = TypeShipping.objects.get(title=post_data['shipping'])
        post_data["shipping_title"] = shipping_text.title
        post_data['shipping_code'] = shipping_text.code
        post_data["calculated_shipping_price"] = shipping_text.price_fix
        face = post_data.get('face', False)
        order_jurical = False
        if face == 'on':
            post_data['jurical'] = True
            order_jurical = True
        payment_file = files.get('file-payment') or ''
        if payment_file:
            filename, file_extension = os.path.splitext(payment_file._name)
            payment_file._name = slugify(
                filename, allow_unicode=True) + file_extension
            post_data["payment_file"] = payment_file
        if shipping_text.show_address and shipping_text.cities:
            if post_data['city'] == '':
                error_list['city'] = 'Укажите нас. пункт'
            if post_data['street'] == '':
                error_list['street'] = 'Укажите улицу'
            if post_data['house'] == '':
                error_list['house'] = 'Укажите дом'
            if post_data['apartment'] == '':
                error_list['apartment'] = 'Укажите квартиру'

        elif shipping_text.show_address:
            if post_data.get('phone') == '':
                error_list['phone'] = 'Укажите телефон'
            if post_data.get("region") == '':
                error_list['region'] = 'Укажите адрес'
            if post_data['entrance'] == '':
                error_list['entrance'] = 'Укажите подъезд'
            if shipping_text.min_price > cart_total:
                error_list['region'] = 'Ошибка, обновите страницу'
            post_data['shipping_type_name'] = post_data['shipping']

        shop_address = post_data.get("shop_address", None)
        if shop_address:
            post_data["shop_address"] = ProductStorage.objects.get(
                pk=shop_address).address
        else:
            post_data["shop_address"] = ProductStorage.objects.first().address

        validated_user = None
        if request.user.is_authenticated:
            validated_user = request.user
        validator = Validator(post_data, validated_user)
        if validator.has_errors:
            if validated_user:
                validated_user = True
            response_context = {
                'errors': True,
                'fields': validator.fields,
                'auth_user': validated_user
            }
            return JsonResponse(response_context)

        if post_data.get('payment') == 'bank' and order_jurical:
            error_list["order"] = "Вы не можете оплатить картой, если заказываете от юр. лица"
            error_list["modal"] = True

        if cart.is_empty:
            error_list["order"] = "Ваша корзина пуста! Обновите страницу"

        if error_list:
            return JsonResponse({
                "errors": True,
                "fields": error_list,
            })

        strategy_class = self.get_strategy()
        strategy = strategy_class(post_data, self.request)
        strategy.execute()
        if strategy.has_errors:
            is_modal_displayed = "display_modal" in strategy.fields
            return JsonResponse({
                "errors": True,
                "fields": strategy.fields,
                "modal": is_modal_displayed
            })
        order = strategy.create_order()
        order.set_date()
        order.status_imported = 'doNotUpload'
        order.save()

        order_info = {
            "ecommerce": {
                "purchase": {
                    "actionField": {
                        "id": str(order.id)
                    },
                    "products": []
                }
            }
        }

        for order_item in order.order_items.all():
            obj = {"id": order_item.product.id,
                   "name": order_item.product.title,
                   "price": float(order_item.product.price),
                   "category": order_item.product.category.title,
                   "quantity": order_item.count}
            order_info["ecommerce"]["purchase"]["products"].append(obj)

        redirect = ""
        if order.type_payment == "bank":
            payment = BankPayment(order, request)
            try:
                if payment.is_valid() and order.is_online_payment_available:
                    redirect = payment.register_payment()
                    order.save_in_stash()
                elif payment.is_valid() and (order.total == 0 or order.is_in_stash):
                    redirect = None
            except BankResponseKeyError:
                print('There is no response from bank')
                order.status_imported = 'doNotUpload'
                order.is_deleted = True
                order.save()
                return JsonResponse({
                    "errors": True,
                    'fields': {
                        'order': 'Ошибка обработки запроса банком, попробуйте позже'
                    },
                    'online_payment_error': True
                })
        self.clear_cart(request, cart)
        order.status_imported = 'not_upload'
        order.save()

        if order.should_send_email:
            send_order_emails(order, request)

        return JsonResponse({
            'redirect': redirect, 'errors': False, 'count': 0,
            'template': get_template(
                template_name='shop/includes/order-success.html').render({
                    'order': order}),
            'ecommerce-product': order_info

        })

    def clear_cart(self, request, cart):
        """Очистка корзины товаров

        Arguments:
            request {object} -- Запрос на сервер
            cart {Cart|UnauthCart} -- Корзина товаров
        """

        if isinstance(cart, Cart):
            cart.items().delete()
        else:
            del request.session['cart']

    def get_cart(self, request):
        """Получить корзину товаров

        Arguments:
            request {object} -- Запрос на сервер
        """

        try:
            if request.user.is_authenticated:
                try:
                    return Cart.objects.get(account__user=request.user)
                except ObjectDoesNotExist:
                    raise 'Корзина не существует'
            return request.session['cart']
        except KeyError:
            raise 'Корзина не существует'

    def get_account(self, cart):
        """Получить пользователя личного кабинета.

        Если пользователь `не найден`, то возвращается `None`.

        Arguments:
            cart {Cart|UnauthCart} -- [description]

        Returns:
            Account|None -- Пользователь личного кабинета
        """

        try:
            return cart.account
        except AttributeError:
            return None

    def get_strategy(self):
        user = self.request.user
        if user.is_authenticated:
            return AuthOrderCreateStrategy
        elif not user.is_authenticated:
            return UnauthOrderCreateStrategy
