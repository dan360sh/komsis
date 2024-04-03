from .BaseDiscount import BaseDiscount


class CollectDiscount(BaseDiscount):

    def execute(self):
        self._cart_count = self._cart.total()
        points_amount = self._account.count_points(self._cart_count)
        self._json_response["message"] = "Количество баллов, которое вы получите после оплаты."
        if not self._account.is_price_type_default:
            self._json_response["extra_message"] = 'Стоимость заказа была пересчитана по розничной цене'
        self._json_response["value"] = points_amount
        self._json_response["new_order_price"] = self._cart_count
        self._json_response["new_products_prices"] = self._get_product_prices()

    def _get_product_prices(self):
        result = dict()
        for cart_item in self._cart.items():
            result[cart_item.id] = cart_item.price()
        return result
