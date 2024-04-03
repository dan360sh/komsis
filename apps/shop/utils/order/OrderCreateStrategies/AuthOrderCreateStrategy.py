from apps.shop.models import Cart, Order, OrderItem
from .UnauthOrderCreateStrategy import UnauthOrderCreateStrategy


class AuthOrderCreateStrategy(UnauthOrderCreateStrategy):

    def execute(self):
        super().execute()
        self._is_order_restored = self._data.get("order_id", False)
        self._is_order_stashed = self._data.get("stash", False)
        self._is_bonus_system_active = self._data.get("bonus_system_active", False)
        if self._is_bonus_system_active and self._is_order_stashed:
            self._is_bonus_system_active = False
        if self._is_bonus_system_active and self._is_order_jurical:
            self._is_bonus_system_active = False

        if self._is_bonus_system_active:
            bonus_system_value = self._data.get("discount", "")
            self._is_points_used = bonus_system_value == "use"
            self._is_points_collected = bonus_system_value == "collect"
        self._cart_total_price = self._calculate_total_price()

        if self._is_bonus_system_active:
            self._validate_points()

    def _get_account(self):
        return self._cart.account

    def _get_cart(self):
        return Cart.objects.get(account__user=self._request.user)

    def _calculate_total_price(self):
        return self._cart.count_total_by_account(self._account) +\
            self._data["calculated_shipping_price"]

    def calculate_order_items_prices(self, order) -> float:
        price = 0
        for el in order.order_items.all():
            price += el.count * el.total
        return round(price, 2)

    def _get_order(self):
        if self._is_order_restored:
            order = self._restore_order()
        else:
            order = self._create_order()

        order.jurical = self._is_order_jurical

        order.status_imported = "not_upload"

        if self._is_order_stashed:
            order.save_in_stash()
            order.status_imported = "doNotUpload"

        self._create_order_items(order)
        order.total = self.calculate_order_items_prices(order)
        order.save()
        price_without_points = order.total
        # Если пользователь не использует бонусную систему вообще
        if not self._is_bonus_system_active:
            order.save()
            return order

        # Если пользователь списывает баллы, то баллы считаются
        # исходя из типа цен пользователя
        if self._is_points_used:
            try:
                points_amount = float(self._data.get('points-value', 0))
            except ValueError:
                points_amount = 0
            redused_price = self._account.calculate_discount(self._cart_total_price, points_amount)
            self._account.reduse_points(points_amount)
            order.total_without_points = price_without_points
            order.total = redused_price
            order.points_spent = points_amount
            order.save()
            return order

        # Если пользователь сохраняет баллы, то добавляем баллы исходя из
        # дефолтного типа цены, в данном случае - розничного
        if self._is_points_collected:
            cart_count = self._cart.total()
            points_to_be_collected = self._account.count_points(cart_count)
            self._account.append_points(points_to_be_collected)
            order.points_collected = points_to_be_collected
            order.total = cart_count
            order.save()
            return order

    def _restore_order(self):
        try:
            order_id = int(self._data.get("order_id"))
        except ValueError:
            order_id = None
        if not order_id:
            raise TypeError("Нет сохраненного заказа")
        order = Order.objects.get(id=order_id)
        order.update_fields(self._data)
        order.order_items.all().delete()
        return order

    def _get_item_price(self, item):
        # Если пользователь копит бонусы с покупки, то считаем
        # позиции закзаа по цене - Розница
        if self._is_bonus_system_active and self._is_points_collected:
            return item.price()

        return item.count_price_by_account(self._account)

    def _validate_points(self):
        try:
            points_amount = float(self._data.get('points-value', 0))
        except ValueError:
            points_amount = 0

        if points_amount > self._cart_total_price:
            self._errors["order"] = "Вы не можете потратить такое кол-во бонусов"

        if not self._account.is_valid_points_amount(points_amount):
            self._errors["order"] = "На вашем аккаунте недостаточно баллов"
