from .DiscountCollect import CollectDiscount
from .DiscountUse import DiscountUse


def get_discount_strategy(discount_state):
    if not discount_state or discount_state == "":
        raise ValueError()

    if discount_state == "use":
        return DiscountUse
    elif discount_state == "collect":
        return CollectDiscount
