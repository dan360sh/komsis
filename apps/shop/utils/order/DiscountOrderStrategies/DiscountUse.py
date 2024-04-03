from .BaseDiscount import BaseDiscount


class DiscountUse(BaseDiscount):
    _redused_points = float()
    _points_amount = float()

    def execute(self):
        self._cart_count = self._cart.count_total_by_account(self._account)
        self._points_amount = self._data.get("points", 0)
        try:
            self._points_amount = float(self._points_amount)
        except ValueError:
            self._points_amount = 0

        self._validate_points()
        if self._json_response.get("errors", False):
            self._has_errors = True

        self._redused_price = self._account.calculate_discount(self._cart_count,
                                                         self._points_amount)
        self._json_response["message"] = 'Сумма к оплате после списания'
        self._json_response['value'] = self._redused_price
        if not self._account.is_price_type_default:
            self._json_response["extra_message"] = "Стоимость заказа была пересчитана по вашему типу цены"
        self._json_response["new_order_price"] = self._cart_count
        self._json_response["new_products_prices"] = self._get_product_prices()

    def _validate_points(self):
        if self._points_amount < 1:
            self._json_response['errors'] = True
            self._json_response["error_message"] = "Вы не можете потратить меньше одного бонуса"

        if not self._account.is_valid_points_amount(self._points_amount):
            self._json_response['errors'] = True
            self._json_response["error_message"] = "На вашем аккаунте нет такого количества бонусов"

        if self._cart_count < self._points_amount:
            self._json_response['errors'] = True
            self._json_response["error_message"] = "Количество бонусов не может превышать стоимость заказа"

    def _get_product_prices(self) -> dict:
        result = dict()
        for cart_item in self._cart.items():
            result[cart_item.id] = cart_item.count_price_by_account(self._account)
        return result
