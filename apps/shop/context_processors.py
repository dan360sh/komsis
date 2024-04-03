from django.core.exceptions import ObjectDoesNotExist

from apps.account.models import Account

from .models import Cart, Compare, Favorites


def cart(request):
    """Добавление в контекст корзины товаров.

    Arguments:
        request {object} -- Запрос на сервер

    Returns:
        dict -- Словарь с данными по корзине
    """

    data = dict()
    if request.user.is_authenticated:
        data['auth'] = True
        data['user'] = request.user
        try:
            # data['account'] = Account.objects.get(user=request.user)
            data['account'] = data['user'].account
            data['cart'] = data['account'].cart
            data['favorites'] = data['account'].favorites
            # data['favorites'] = Favorites.objects.get(
            #     account__user=request.user)
            # data['compare'] = Compare.objects.get(
            #     account__user=request.user)
            data['favorites_list'] = data['favorites'].favorites_items.values_list(
                'product__id', flat=True)
            # data['favorites_list'] = [item.product.id for item in Favorites.objects.get(account__user=request.user).items()]
            # data['compare_list'] = [item.product.id for item in Compare.objects.get(account__user=request.user).items()]
        except ObjectDoesNotExist:
            data['cart'] = None
            data['favorites'] = None
            data['compare'] = None

    else:
        data['account'] = None
        data['auth'] = False
        try:
            data['cart'] = request.session['cart']
        except KeyError:
            data['cart'] = None
        try:
            data['favorites'] = request.session['favorites']
            data['favorites_list'] = [
                k.product.id for k in request.session['favorites'].items()]
        except KeyError:
            data['favorites'] = None
        try:
            data['compare'] = request.session['compare']
            data['compare_list'] = [
                k.product.id for k in request.session['compare'].items()]
        except KeyError:
            data['compare'] = None
    return data
