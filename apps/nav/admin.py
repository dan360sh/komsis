from django.contrib import admin
from django import forms

from mptt import admin as mptt_admin
from mptt import forms as mptt_forms
from django_mptt_admin.admin import DjangoMpttAdminMixin
from ajax_select.fields import AutoCompleteSelectField

from .models import Navigation


class NavigationForm(mptt_forms.MPTTAdminForm):
    object_href = AutoCompleteSelectField('hrefs', required=False, label="Объект-ссылка")
    model = Navigation

    def clean(self):
        super(NavigationForm, self).clean()
        if not(self.cleaned_data['alias'] or self.cleaned_data['href'] or self.cleaned_data['object_href']):
            raise forms.ValidationError("Объект никуда не указывает")


class NavigationInline(admin.TabularInline):
    model = Navigation
    form = NavigationForm
    extra = 0


class NavigationAdmin(DjangoMpttAdminMixin, mptt_admin.DraggableMPTTAdmin):
    inlines = [NavigationInline]
    form = NavigationForm
    list_display = ('tree_actions', 'indented_title', 'href', 'object_href')
    list_editable = ('href', 'object_href')


admin.site.register(Navigation, NavigationAdmin)
