from django.contrib import admin
from .models import Settings, City, Slider, TypeShipping, PhoneNumber, ContactEmail


class SliderInline(admin.TabularInline):
    model = Slider
    extra = 1


class CityInline(admin.TabularInline):
    model = City
    extra = 1

class SettingsAdmin(admin.ModelAdmin):
    list_display = ('language', 'name')
    readonly_fields = ('color_scheme_alpha', 'color_scheme_dark')
    fieldsets = (
        (None, {'fields': (
            'language',
            'name',
            'color_scheme',
            'color_scheme_alpha',
            'color_scheme_dark',
            'in_product_view',
        )}),
        ("Контакты", {'fields': (
            'full_address',
            'address',
            'phones',
            'email',
            'time_work',
            'time_work_cherep',
            ('coord_x', 'coord_y'),
            'price_list',
            'privacy_policy',
            'personal_data',
            'banner_text',
            'banner_img',
            'payment_text',
            'shipping_text'
        )}),
        ("Социальные сети", {'fields': (
            'social_view',
            'vkontakte',
            'facebook',
            'instagram',
            'telegram',
            'twitter',
            'youtube',
            'odnoklassniky',
        )}),
        ("SEO", {'fields': (
            'seo_text',
            'seo_img1',
            'seo_img2',
            'seo_img3',
            'meta_title',
            'meta_template_title',
            'meta_description',
            'meta_template_description',
            'meta_keywords',
            'head_scripts',
            'scripts',
            'robots_txt',
        )}),
        ("Оплата", {'fields': (
            'mode_payment',
            'shop_id',
            'api_key',
        )}),
        ("bitrix24", {'fields': (
            'bitrix24_key',
            'bitrix24_domain',
        )}),

    )
    inlines = [CityInline, SliderInline]


class TypeShippingAdmin(admin.ModelAdmin):
    pass


class PhoneNumberInline(admin.TabularInline):
    model = PhoneNumber
    extra = 0


class EmailInline(admin.TabularInline):
    model = ContactEmail
    extra = 0


class CityAdmin(admin.ModelAdmin):
    inlines = (PhoneNumberInline, EmailInline)


admin.site.register(Settings, SettingsAdmin)
admin.site.register(TypeShipping, TypeShippingAdmin)
admin.site.register(City, CityAdmin)
