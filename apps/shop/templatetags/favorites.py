from django import template

register = template.Library()


@register.simple_tag
def product_waiting(product, favorites):
    """Шаблонный тег для проверки наличия товара в списке ожидаемых товаров.

    Arguments:
        product {Product} -- Товар
        favorites {Favorites|UnauthFavorites} -- Модель или простой класс
            избранных товаров

    Returns:
        bool -- Наличие товара в списке ожидаемых
    """

    for item in favorites.items():
        if item.product == product and item.waiting:
            return True
    return False
