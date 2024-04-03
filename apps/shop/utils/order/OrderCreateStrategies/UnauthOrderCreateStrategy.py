from apps.account.models import Account
from apps.shop.models.order import OrderItem

from .BaseOrderStrategy import BaseOrderStrategy


class UnauthOrderCreateStrategy(BaseOrderStrategy):
    _account = None
    _cart = None
    _cart_total_price = None
    _is_order_jurical = False
    _order = None

    def __init__(self, post_data, request) -> None:
        super().__init__(post_data, request)

    def execute(self):
        self._cart = self._get_cart()
        self._account = self._get_account()
        self._cart_total_price = self._calculate_total_price()
        self._is_order_jurical = self._data.get("jurical", False)

    def create_order(self):
        return self._get_order()

    def _get_cart(self):
        return self._request.session['cart']

    def _calculate_total_price(self):
        return self._cart.count_total_by_account(None) + self._data["calculated_shipping_price"]

    def _get_account(self):
        email = self._data["email"]
        user = Account.register(email,
                                "{}://{}".format(self._request.scheme,
                                                 self._request.META['HTTP_HOST']),
                                send_mail=True)
        if not user:
            raise ValueError("Аккаунт уже существует")
        Account.auth(self._request, user)
        user.account.name = self._data["name"]
        user.account.surname = self._data["surname"]
        user.account.phone = self._data.get("phone") or ''
        user.account.email = self._data["email"]
        user.account.jurical = self._data.get('jurical', False)
        user.account.company_title = self._data.get('company_title') or ''
        user.account.company_inn = self._data.get('company_inn') or ''
        user.account.save()
        account = user.account
        return account

    def _get_order(self):
        order = super()._get_order()
        order.jurical = self._is_order_jurical
        self._create_order_items(order)
        order.total = self.calculate_order_items_prices(order)
        order.save()
        return order

    def calculate_order_items_prices(self, order) -> float:
        price = 0
        for el in order.order_items.all():
            price += el.count * el.total
        return round(price, 2)

    def _create_order_items(self, order):
        for item in self._cart.items():
            item_total_price = self._get_item_price(item)
            option = item.option if item.option else None
            count = item.count
            if item.count >= item.product.count:
                count = item.product.count
                order.comment += f"\nДля товара {item.product.title} покупателю требуется количество {item.count}."
                order.save()
            OrderItem.objects.create(
                order=order,
                product=item.product,
                option=option,
                count=count,
                total=item_total_price,
            )

    def _get_item_price(self, item):
        return item.count_price_by_account(None)
