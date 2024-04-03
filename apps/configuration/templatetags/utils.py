from apps.configuration.models.email import ContactEmail
from apps.shop.models import Cart
from django import template
from django.template.defaultfilters import floatformat

register = template.Library()


@register.filter(name='format_date')
def format_date(value, format_string="%d.%m.%Y"):
    return value.strftime(format_string)


@register.filter(name='formatted_float')
def formatted_float(value):
    value = floatformat(value, arg=4)
    return str(value).replace(',', '.')


@register.filter(name='format_number')
def formatted_float(value):
    try:
        if int(value) == float(value):
            return '{:,.0f}'.format(float(value)).replace(',', ' ')
        return '{:,.1f}'.format(float(value)).replace(',', ' ')
    except:
        pass


@ register.filter(name='alt')
def get_alt(value):
    if value:
        if value.default_alt_text:
            return value.default_alt_text
        else:
            return value.original_filename
    return ""


@ register.simple_tag(takes_context=True)
def get_product_price(context):
    product = get_product(context)
    user = context['request'].user
    account = user.account if user.is_authenticated else None
    return product.get_price_by_account(account)


@ register.simple_tag(takes_context=True)
def get_option_price(context):
    option = get_option(context)
    user = context.get("request", None).user
    account = user.account if user.is_authenticated else None
    return option.get_price_by_account(account)


@ register.simple_tag(takes_context=True)
def get_min_option_price(context):
    product = get_product(context)
    user = context.get("request").user
    first_option = product.options.filter(
        active=True, price__gt=0
    ).order_by("price").first()
    account = user.account if user.is_authenticated else None
    return product.get_price_by_account(account)


@ register.simple_tag(takes_context=True)
def get_old_price(context):
    product = get_product(context)
    user = context['request'].user
    account = user.account if user.is_authenticated else None
    return product.get_old_price(account)


@ register.simple_tag(takes_context=True)
def on_sale(context):
    product = get_product(context)
    user = context['request'].user
    # Откуда-то приходит строка "х"
    if isinstance(product, str):
        return False
    account = user.account if user.is_authenticated else None
    return product.on_sale(account) and product.has_count


@ register.simple_tag(takes_context=True)
def get_item_total_price(context):
    item = context['item']
    user = context['request'].user
    if not user.is_authenticated:
        return item.total()
    account = user.account if user.is_authenticated else None
    return item.count_total_by_account(account)


@ register.simple_tag(takes_context=True)
def count_cart(context):
    cart = context['cart']
    user = context['request'].user
    # if not user.is_authenticated:
    #     return cart.total
    account = user.account if user.is_authenticated else None
    return cart.count_total_by_account(account)


def get_product(context):
    product = context.get('product', None)
    if product:
        return product

    # Получить инстанс Продукта
    # Например, CartItem
    item = context['item']
    return item.product


def get_option(context):
    option = context.get("option", None)
    if option:
        return option

    item = context["item"]
    return item.option


@ register.simple_tag(takes_context=True)
def get_default_points(context):
    max_amount = get_max_points(context)
    if max_amount < 1:
        return 0
    return round(max_amount / 2, 2)


@ register.simple_tag(takes_context=True)
def get_max_points(context):
    request = context['request']
    user = request.user

    if not user.is_authenticated:
        cart = context['request'].session['cart']
        return cart.total()

    account = user.account
    cart = Cart.objects.get(account=account)
    if not account.points_total:
        if account.is_price_type_default:
            return cart.total()
        return cart.count_total_by_account(account)

    cart_total_by_price_type = cart.count_total_by_account(account)

    if account.points_total > cart_total_by_price_type:
        return cart_total_by_price_type

    return account.points_total


@ register.simple_tag(takes_context=False)
def get_emails():
    return ContactEmail.objects.order_by("sort", "email", "title").distinct("sort", "email", "title")
