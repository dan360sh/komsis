from django.contrib import admin

from mptt import admin as mptt_admin
from django_mptt_admin.admin import DjangoMpttAdminMixin

from apps.seo.admin import SeoAdminMixin
from .models import (Page, Offer, Vacancy)


class PageAdmin(DjangoMpttAdminMixin, mptt_admin.DraggableMPTTAdmin):
    list_display = ('id', 'tree_actions', 'indented_title', 'parent', 'active')
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        (None, {'fields': (
            'active',
            'title',
            'slug',
            'parent',
            'original',
            'content',
            'template'
        )}),
        ("SEO", {'fields': SeoAdminMixin.seo_fields}),
    )


class OfferAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Page, PageAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Vacancy)
