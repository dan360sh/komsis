from django.urls import path

from .views import (ContactsFormView, OrderServiceView, QuestionView,
                    SubscribeView)

urlpatterns = [
    # Обработка запроса на добавление товара в конзину
    path('api/feedback/subscribe/',
         SubscribeView.as_view(),
         name='feedback-subscribe'),
    path('api/feedback/question/',
         QuestionView.as_view(),
         name='feedback-question'),
    path('api/feedback/contacts/',
         ContactsFormView.as_view(),
         name='feedback-contacts'),
    path('api/feedback/order-service/',
         OrderServiceView.as_view(),
         name='order-service'),
]
