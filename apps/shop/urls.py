from django.urls import path

from .views import (AddCompareView, AddFavoritesView, AddWaitingFavoritesView,
                    AvailableView, CalculateShippingView, CartAddView,
                    CartDeleteView, CartTemplate, CartUpdateView, CompareView,
                    DeleteCompareView, DeleteFavoritesView, FavoritesView,
                    OrderCreate, OrderView, PaymentRedirectView,
                    RestoreCompareView, RestoreFavoritesView)

urlpatterns = [
    path('shop/cart/', CartTemplate.as_view(), name='cart'),
    path('shop/order/', OrderView.as_view(), name='order'),
    path('shop/favorites/', FavoritesView.as_view(), name='favorites'),
    path('shop/compare/', CompareView.as_view(), name='compare'),
    path('shop/validate-payment/',
         PaymentRedirectView.as_view(), name='validate-payment'),

    # Ajax обработчики

    path('api/shop/cart/available/', AvailableView.as_view(), name='available'),
    path('api/shop/order/calculate/',
         CalculateShippingView.as_view(), name='calculate-shipping'),
    path('api/shop/cart/add/', CartAddView.as_view(), name='cart-add'),
    path('api/shop/cart/update/', CartUpdateView.as_view(),
         name='cart-update'),
    path('api/shop/cart/delete/', CartDeleteView.as_view(),
         name='cart-delete'),
    path('api/shop/order/create/', OrderCreate.as_view(),
         name='order-create'),
    path('api/shop/favorites/add', AddFavoritesView.as_view(),
         name='favorites-add'),
    path('api/shop/favorites/delete', DeleteFavoritesView.as_view(),
         name='favorites-delete'),
    path('api/shop/favorites/restore', RestoreFavoritesView.as_view(),
         name='favorites-restore'),
    path('api/shop/favorites/add-waiting',
         AddWaitingFavoritesView.as_view(),
         name='favorites-add-waiting'),
    path('api/shop/compare/add', AddCompareView.as_view(),
         name='compare-add'),
    path('api/shop/compare/delete', DeleteCompareView.as_view(),
         name='compare-delete'),
    path('api/shop/compare/restore', RestoreCompareView.as_view(),
         name='compare-restore'),
]
