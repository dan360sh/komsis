from django.urls import path
from django.views.generic.base import TemplateView

from .views import (ContactsPage, IndexView, OffersView, OfferView, PageView,
                    VacanciesView, VacancyMail)

urlpatterns = [
    # Главная страница
    path('', IndexView.as_view(), name="index"),

    # Прочие страницы
    path('contacts/', ContactsPage.as_view(), name="contacts"),
    path('offers/', OffersView.as_view(), name="offers"),
    path('offer/<slug>/', OfferView.as_view(), name="offer"),
    path('privacy-policy/', TemplateView.as_view(
        template_name="privacy-policy.html"), name="privacy-policy"),
    path('personal-data/', TemplateView.as_view(
        template_name="personal-data.html"), name="personal-data"),
    path('vacancies/', VacanciesView.as_view(), name="vacancies"),
    # Динамические страницы
    path('<slug>/', PageView.as_view(), name='page'),

    # API
    path('api/vacancymail/', VacancyMail.as_view(), name="vacancymail"),
]
