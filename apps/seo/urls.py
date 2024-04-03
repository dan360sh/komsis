from django.urls import path

# from .sitemap import sitemaps
from .views import robots

# from django.contrib.sitemaps.views import sitemap


urlpatterns = [
    path('robots.txt', robots, name="seo-robots"),
]
