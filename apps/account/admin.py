from django.contrib import admin
from .models import Account, Manager, DiscountCard, AccountStatus
from django.utils.html import format_html


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_filter = ('jurical',)
    search_fields = (
        'user__username', 'email',
        'name', 'company_title', 'company_inn',
        'phone', 'surname', 'middle_name', "clear_name"
    )
    list_display = (
        'display_username', 'email',
        'jurical', 'price_type'
    )
    fieldsets = (
        (None, {
            'fields': ('jurical', 'manager', 'user', 'status',
            'price_type', 'discount_card', 'points_total', 'unconfirmed_points')
        }),
        ('Информация об аккаунте', {
            'fields': (
                'surname', 'name', 'middle_name', 'clear_name',
                'email', 'phone', 'valid_phone', 'company_title',
                'company_inn', 'bonus_card_id', "purchase_sum",
                'contract_name', 'contract_type', 'contract_balance'
            )
        })
    )
    readonly_fields = ['valid_phone', ]

    def display_username(self, obj):
        color = '#FFA500' if obj.jurical else ''
        username = obj.full_name if obj.name != '' else obj.user.username
        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            username,
        )
    display_username.short_description = 'Имя пользователя'


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    search_fields = (
        'name', 'email',
        'phone'
    )
    list_display = ('name', 'email', 'phone')


@admin.register(DiscountCard)
class DiscountCardAdmin(admin.ModelAdmin):
    list_display = ('title', 'percent')


@admin.register(AccountStatus)
class AccountStatusAdmin(admin.ModelAdmin):
    list_display = ("title", "min_limit", "max_limit")
