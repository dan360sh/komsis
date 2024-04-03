from apps.catalog.models import CategorySitemap, ProductSitemap
from apps.pages.views import return_js
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps.views import sitemap
#
from django.urls import include, path, reverse
#  delete later
from django.views.generic import RedirectView, TemplateView


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['catalog', ]

    def location(self, item):
        return reverse(item)


sitemaps = {
    'products': ProductSitemap,
    'categorys': CategorySitemap,
    # 'posts': SitemapCatPage,
    # 'catsposts': SitemapPost,
    # 'pages': SitemapPage,
    'static': StaticViewSitemap
}

urlpatterns = [
    path('favicon.ico',
         RedirectView.as_view(url='/static/images/favicon.png'),
         name='favicon'),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),

    path('admin/', admin.site.urls),

    # Прочие приложения
    path('filer/', include('filer.urls')),
    path('ajax_lookup/', include('ajax_select.urls'),
         name='ajax_lookup'),
    path('ckeditor/', include('ckeditor_uploader.urls')),

    # delete later
    path('dev_page', TemplateView.as_view(
        template_name="dev_page.html"), name='dev_page'),
    path('dev_text_page', TemplateView.as_view(
        template_name="dev_text_page.html"), name='dev_page'),
    # path('404', not_found_view),

    path('sw.js', return_js),

    # Основные приложения
    path('', include('apps.seo.urls')),
    path('', include('apps.feedback.urls')),
    path('', include('apps.exchange1c.urls')),
    path('', include('apps.catalog.urls')),
    path('', include('apps.account.urls')),
    path('', include('apps.shop.urls')),
    path('', include('apps.pages.urls')),
    path('', include('apps.posts.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
