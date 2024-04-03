from apps.shop.models import Order, OrderItem, OrderState
from apps.configuration.models import TypeShipping
from abc import ABC, abstractmethod


class AbstractOrderStrategy(ABC):

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def _get_cart(self):
        pass

    @abstractmethod
    def _get_order(self):
        pass

    @abstractmethod
    def _get_account(self):
        pass

    @abstractmethod
    def _create_order_item(self, cart_item):
        pass

    @abstractmethod
    def _calculate_total_price(self):
        pass


class BaseOrderStrategy(AbstractOrderStrategy):

    def __init__(self, post_data, request) -> None:
        self._data = post_data
        self._request = request
        self._errors = dict()

    @property
    def has_errors(self):
        return len(self._errors) > 0

    @property
    def fields(self):
        return self._errors

    def _get_order(self):
        return self._create_order()

    def _create_order(self):
        order: Order = Order.objects.create(
                account=self._account,
                name=self._data['name'],
                surname=self._data['surname'],
                middle_name=self._data.get('middle_name', ''),
                email=self._data['email'],
                post_code=self._data.get('post_code', 0),
                district=self._data.get('district', ''),
                city=self._data.get('city', ''),
                street=self._data.get('street', ''),
                house=self._data.get('house', ''),
                housing=self._data.get('housing', ''),
                apartment=self._data.get('apartment', ''),
                comment=self._data.get('comment', ''),
                type_payment=self._data.get('payment'),
                shipping_price=self._calculate_shipping(),
                company_title=self._data.get('company_title') or '',
                company_inn=self._data.get('company_inn') or '',
                phone=self._data.get('phone'),
                payment_file=self._data.get("payment_file", None),
                status='processing',
                status_imported='not_upload',
                shipping_type_name=self._data["shipping_title"],
                shipping=self._data["shipping_code"],
                shop_address=self._data.get("shop_address", None),
                region=self._data.get('region', ''),
                entrance=self._data.get('entrance', ''),
            )
        order.total = self._calculate_total_price()
        order.completed_states.add(OrderState.default())
        order.save()
        return order

    def _calculate_shipping(self):
        shipping_type = TypeShipping.objects.get(
            title=self._data['shipping_title']
        )
        return shipping_type.price_fix

    def _calculate_total_price(self):
        raise NotImplementedError("")

    def _create_order_item(self, item):
        item_total_price = item.price()
        OrderItem.objects.create(order=self._order, product=item.product,
                                 count=item.count, total=item_total_price)
