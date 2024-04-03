import os

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Case, Count, IntegerField, Sum, Value, When
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import render
from django.utils.text import slugify
from django.views.generic import ListView, TemplateView, View
from django.views.generic.detail import DetailView

from apps.catalog.models import Brand, Direction, Product
from apps.catalog.models.index_blocks import IndexBlock
from apps.configuration.context_processors import website_settings
from apps.configuration.models import City, Settings, Slider
from apps.feedback.models import Email
from apps.feedback.utils import template_email_message
from apps.posts.models import Category, Post

from .forms import VacancyForm
from .models import Offer, Page, Vacancy


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        request = self.request
        user = request.user
        account = None
        if user.is_authenticated:
            account = user.account

        context['slider'] = Slider.objects.select_related('image').all()
        context["mobile_slider"] = Slider.objects\
            .select_related("mobile_image").filter(mobile_image__isnull=False)

        hit_products = Product.with_options.annotate_options().filter(hit=True)
        new_products = Product.with_options.annotate_options().filter(new=True)
        sale_products = Product.sale_filter(
            Product.with_options.annotate_options())
        if account:
            if not account.is_price_type_default:
                hit_products = hit_products.filter(
                    prices__type=account.price_type)
                new_products = new_products.filter(
                    prices__type=account.price_type)
                sale_products = sale_products.filter(
                    prices__type=account.price_type)
        context['hit_products'] = hit_products[:7]
        context['new_products'] = new_products[:7]
        context['sale_products'] = sale_products[:7]
        #Product.objects.filter( active=True, sale=True).order_by('?')[0:7]
        context['brands'] = Brand.objects.select_related('thumbnail').all()[
            0:12]

        # context['directions'] = Direction.objects.all()[:12]

        context['directions'] = Direction.objects.annotate(
            products_count=Sum(
                Case(
                    When(
                        direction_products__active=True,
                        then=Value(1)
                    ),
                    default=Value(0),
                    output_field=IntegerField()
                )
            )
        ).select_related('thumbnail').all()[:12]

        context['index_page_blocks'] = IndexBlock.objects.filter(
            is_active=True
        ).order_by('sort')
        # offers = Offer.objects.filter(active=True).order_by("-date")[:2]
        # if offers.count() == 2:
        #     context['offers'] = offers
        # else:
        #     context['offers'] = []
        return context


class PageView(DetailView):
    context_object_name = 'page'
    model = Page
    template_name = 'pages/page.html'


class OffersView(ListView):
    model = Offer
    context_object_name = 'offers'
    template_name = 'pages/offers.html'
    try:
        queryset = Offer.objects.filter(active=True)
    except ObjectDoesNotExist:
        queryset = False

    def get_context_data(self, **kwargs):
        context = super(OffersView, self).get_context_data(**kwargs)
        context['object'] = Page.objects.get(template=1)
        return context


class OfferView(DetailView):
    context_object_name = 'offer'
    model = Offer
    template_name = 'pages/offer.html'


class ContactsPage(TemplateView):
    context_object_name = 'contacts'
    template_name = 'pages/contacts.html'

    def get_context_data(self, **kwargs):
        context = super(ContactsPage, self).get_context_data(**kwargs)
        context['object'] = Page.objects.get(template=2)
        return context


def not_found_view(request, _):
    web_settings = website_settings(request)
    response = render(request, '404.html', web_settings)
    return HttpResponseNotFound(response)


def return_js(request):
    response = render(
        request, 'sw.js', {}, content_type='application/javascript')
    return response


class VacanciesView(ListView):
    model = Vacancy
    context_object_name = 'vacancy_list'
    template_name = 'pages/vacancies.html'
    queryset = Vacancy.objects.all().order_by('sort')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["city_list"] = City.objects.all()
        return context


class VacancyMail(View):

    def post(self, request):
        data = request.POST
        error = False
        message = 'Ждите звонка'
        res = [item.title for item in Email.objects.all()]
        file = request.FILES.get('sumfile', None)
        if file:
            filename, file_extension = os.path.splitext(file._name)
            file._name = slugify(filename, allow_unicode=True) + file_extension

        try:
            template_email_message(
                'pages/vacancy_mail.html',
                subject='Подано резюме от: {name}!'.format(name=data['name']),
                to=res,
                data={
                    'name': data['name'],
                    'phone': data['phone'],
                    'position': data['position']
                },
                file=file
            )

        except Exception as e:
            message = str(e.with_traceback())
            error = True
            # raise e

        return JsonResponse({'error': error, 'message': message})
