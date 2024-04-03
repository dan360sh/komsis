from ajax_select.fields import AutoCompleteSelectField
from django import forms
from django.contrib import admin

from apps.shop.models.order import OrderLog

from .models import Order, OrderItem, OrderState


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    exclude = ('product',)
    readonly_fields = ('product', 'color', 'option')


class OrderLogInline(admin.TabularInline):
    model = OrderLog
    extra = 0
    readonly_fields = ('date',)


class OrderForm(forms.ModelForm):
    account = AutoCompleteSelectField('account', required=False,
                                      label="Профиль")


class OrderAdmin(admin.ModelAdmin):
    form = OrderForm
    inlines = [OrderItemInline, OrderLogInline]
    list_display = ['__str__', 'display_username', 'email', 'date', 'total']
    fieldsets = (
        (None, {
            'fields': (
                'account',
                'surname', 'name', 'middle_name', 'email',
                'phone', 'comment', 'jurical', 'company_title', 'company_inn',
                'payment_file', 'is_deleted', "completed_states")
        }),
        ('Основная информация по заказу', {
            'fields': (
                'status', 'current_state', 'date',
                'status_imported', 'shop_address',
            )
        }),
        ('Информация по оплате', {
            'fields': (
                'payment', 'is_confirmed', 'type_payment', 'total', 'bank_id',
                'total_without_points', 'points_spent',
                'points_collected'
            )
        }),
        ('Информация по доставке', {
            'fields': (
                'shipping', 'shipping_price',
                'post_code', 'region',
                'district', 'city',
                'street', 'house', 'housing',
                'apartment', 'entrance',
                'shipping_type_name',
                # 'shop_address'
            )
        })
    )
    readonly_fields = ("is_confirmed", )

    def display_username(self, obj):
        return f"{obj.surname} {obj.name} {obj.middle_name}"
    display_username.short_description = "ФИО пользователя"


class OrderStateAdmin(admin.ModelAdmin):
    list_display = ("title", "code", "position")


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderState, OrderStateAdmin)
