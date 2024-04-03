from apps.catalog.models import Product
from django.http import JsonResponse
from django.template.loader import get_template
from django.views.generic import TemplateView, View

from ..models import (Favorites, FavoritesItem, UnauthFavorites,
                      UnauthFavoritesItem)


class FavoritesView(TemplateView):
    """Представление странцы избранных товаров магазина"""

    template_name = 'shop/favorites.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favorites_page'] = True
        return context


class AddFavoritesView(View):
    """Представление добавления товара в избранные"""

    def post(self, request):
        post_data = request.POST
        product = Product.objects.get(id=int(post_data['product']))

        # Добавление в избранные
        if request.user.is_authenticated:
            favorites = self.update_auth_favorites(request, product)
        else:
            favorites = self.update_unauth_favorites(request, product)

        return JsonResponse({'count': favorites.count()})

    def update_auth_favorites(self, request, product):
        """Добавление товара в избранные товары авторизованного пользователя.

        Arguments:
            request {object} -- Запрос на сервер
            product {Product} -- Товар

        Returns:
            Favorites -- Экземпляр модели избранных товаров авторизванного
            пользователя
        """

        favorites = Favorites.objects.filter(
            account__user=self.request.user).first()
        favorites_item, created = FavoritesItem.objects.get_or_create(
            favorites=favorites, product=product)
        if not created:
            favorites_item.delete()
        return favorites

    def update_unauth_favorites(self, request, product):
        """Добаление товара в избранные товары не авторизованного
        пользователя(избранные добавляется в сессию).

        Arguments:
            request {object} -- Запрос на сервер
            product {Product} -- Товар

        Returns:
            UnauthFavorites -- Избранные товары не авторизванного пользователя
        """

        favorites = request.session.get('favorites', None)
        if favorites:
            found_item = False
            for item in favorites.favorites_items:
                if item.product == product:
                    found_item = True
            if not found_item:
                favorites.favorites_items.append(
                    UnauthFavoritesItem(product=product))
        else:
            favorites = UnauthFavorites(
                favorites_items=[UnauthFavoritesItem(product=product)])
        request.session['favorites'] = favorites
        request.session.save()
        return favorites


class DeleteFavoritesView(View):
    """Представление удаления товара из избранных"""

    def post(self, request):
        post_data = request.POST
        product = Product.objects.get(id=int(post_data['product']))

        # Добавление в избранные
        if request.user.is_authenticated:
            favorites = self.update_auth_favorites(request, product)
        else:
            favorites = self.update_unauth_favorites(request, product)

        restore = get_template(
            template_name='shop/includes/favorites-restore.html').render(
                {'product': product})

        return JsonResponse({'count': favorites.count(), 'restore': restore})

    def update_auth_favorites(self, request, product):
        favorites = Favorites.objects.get(account__user=request.user)
        FavoritesItem.objects.filter(
            favorites=favorites, product=product).first().delete()
        return favorites

    def update_unauth_favorites(self, request, product):
        favorites = request.session.get('favorites', None)
        for key, item in enumerate(favorites.favorites_items):
            if item.product == product:
                del favorites.favorites_items[key]
        request.session['favorites'] = favorites
        request.session.save()
        return favorites


class RestoreFavoritesView(View):
    """Представление восстановления товара в избранных"""

    def post(self, request):
        post_data = request.POST
        product = Product.objects.get(id=int(post_data['product']))

        # Добавление в избранные
        if request.user.is_authenticated:
            favorites = self.update_auth_favorites(request, product)
        else:
            favorites = self.update_unauth_favorites(request, product)

        return JsonResponse({'count': favorites.count()})

    def update_auth_favorites(self, request, product):
        favorites = Favorites.objects.get(account__user=request.user)
        FavoritesItem.objects.update_or_create(
            favorites=favorites, product=product)
        return favorites

    def update_unauth_favorites(self, request, product):
        favorites = request.session.get('favorites', None)
        favorites.favorites_items.append(UnauthFavoritesItem(product=product))
        request.session['favorites'] = favorites
        request.session.save()
        return favorites


class AddWaitingFavoritesView(View):
    """Представление добавления товара в лист ожидание избранных товаров"""

    def post(self, request):
        post_data = request.POST
        product = Product.objects.get(id=int(post_data['product']))
        favorites = Favorites.objects.get(account__user=request.user)
        favorites_item, created = FavoritesItem.objects.get_or_create(
            favorites=favorites, product=product)
        if favorites_item.waiting:
            favorites_item.waiting = False
        else:
            favorites_item.waiting = True
        favorites_item.save()
        return JsonResponse({'count': favorites.count()})
