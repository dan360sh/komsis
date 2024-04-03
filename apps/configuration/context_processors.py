from django.db.models import Q, Prefetch

from apps.catalog.models import Category
from apps.nav.models import Navigation
from .models import Settings
from django.utils import timezone


def website_settings(request):
    data = {}

    queryset_settings = Settings.objects.all()
    if request.path == '/':
        queryset_settings = queryset_settings.select_related('seo_img1', 'seo_img2', 'seo_img3')
    web_settings = queryset_settings.filter(
        language=request.LANGUAGE_CODE).first()
    if not web_settings:
        web_settings = queryset_settings.first()
        if not web_settings:
            web_settings = Settings(language='fallback')

    # data['categories'] = Category.objects.filter(parent=None, active=True).order_by('title')

    data['categories'] = Category.objects.prefetch_related(
        Prefetch("childs", Category.objects.filter(active=True).only("title", "slug", "parent").order_by("title"))
    ).filter(parent=None, active=True).only("title", "slug", "parent").order_by("title")
    data['header_menu'] = Navigation.objects.filter(parent=None)

    data['SERVER'] = request
    data['SERVER_DICT'] = request.__dict__
    data['SERVER_GET'] = request.GET
    data['SERVER_META'] = request.META
    data['SERVER_SESSION'] = request.session
    data['SERVER_SESSION_DICT'] = request.session.__dict__

    data['settings'] = web_settings

    date_modal_open = request.session.get('has_modal_open')
    if not date_modal_open:
        request.session['has_modal_open'] = timezone.now()
        data['days'] = 1
    else:
        data['days'] = (timezone.now() - date_modal_open).days
        if data['days'] > 0:
            request.session['has_modal_open'] = timezone.now()
    return data
