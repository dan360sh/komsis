from django.contrib.auth.views import (PasswordChangeDoneView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetView)
from django.urls import path, reverse_lazy

from .views import (ChangeDataView, ChangePasswordView, CreateAccountView,
                    CustomPasswordResetConfirmView,
                    CustomPasswordResetDoneView, CustomPasswordResetView,
                    DataTemplate, FavoritesTemplate, FavoritesWaitingList,
                    JuricalOrdersList, LoginView, LogoutView, OrderDeleteView,
                    OrderDetail, OrderItemDeleteView, OrdersList,
                    OrderToPdfView, OrderUpdateView, PasswordTemplate,
                    RegisterView, SubscribeAddView, SubscribeTemplate)

app_name = "accounts"
urlpatterns = [
    path(
        'account/register/',
        CreateAccountView.as_view(),
        name='account-create'
    ),
    path('account/orders/', OrdersList.as_view(), name='account-orders'),
    path('account/orders/jurical/', JuricalOrdersList.as_view(),
         name='account-orders-jurical'),
    path('account/orders/<int:pk>/',
         OrderDetail.as_view(), name='account-order'),
    path('account/data/', DataTemplate.as_view(), name='account-data'),
    path('account/favorites/', FavoritesTemplate.as_view(),
         name='account-favorites'),
    path('account/waiting/', FavoritesWaitingList.as_view(),
         name='account-waiting'),
    path('account/password/', PasswordTemplate.as_view(),
         name='account-password'),
    path('account/subscribe/', SubscribeTemplate.as_view(),
         name='account-subscribe'),

    # Ajax обработчики

    path('api/account/login/', LoginView.as_view(),
         name='account-login'),
    path('api/account/orders/<int:pk>/remove/', OrderDeleteView.as_view(),
         name='order-delete'),
    path('api/account/orders/<int:pk>/update/', OrderUpdateView.as_view(),
         name='order-update'),
    path('api/account/orders/<int:pk>/item/remove/', OrderItemDeleteView.as_view(),
         name='order-item-delete'),
    path('api/account/orders/<int:pk>/pdf/', OrderToPdfView.as_view(),
         name='order-to-pdf'),
    path('api/account/register/', RegisterView.as_view(),
         name='account-register'),
    path('api/account/logout/', LogoutView.as_view(),
         name='account-logout'),
    path('api/account/data/change/', ChangeDataView.as_view(),
         name='account-change-data'),
    path('pi/account/subscribe/add/', SubscribeAddView.as_view(),
         name='account-subscribe-add'),
    path('api/account/password/change/', ChangePasswordView.as_view(),
         name='account-change-password'),

    path(
        'user/password/reset/',
        CustomPasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        'user/password/reset/done/',
        CustomPasswordResetDoneView.as_view(), name="password_reset_done"
    ),
    path(
        'user/password/reset/<slug:uidb64>/<slug:token>/',
        CustomPasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),

    path('user/password/done/',
         PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
