from ajax_select.admin import AjaxSelectAdmin, AjaxSelectAdminTabularInline
from ajax_select.fields import AutoCompleteSelectField, autoselect_fields_check_can_add
from django import forms
from django.contrib import admin, messages
from django_mptt_admin.admin import DjangoMpttAdmin
from mptt.admin import MPTTModelAdmin
from import_export.formats import base_formats

from apps.seo.admin import SeoAdminMixin

from . import models
from import_export import resources
from import_export.admin import ExportActionMixin


class CategoryResources(resources.ModelResource):
    class Meta:
        model = models.Category


class CategoryAdmin(ExportActionMixin, SeoAdminMixin, DjangoMpttAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "active",
                    "display_in_categories",
                    "black_color",
                    "display_nested_filters",
                    "display_related_categories_and_filters",
                    "display_related_categories",
                    "unloading_id",
                    "title",
                    "slug",
                    "parent",
                    "thumbnail",
                    "alt_title",
                    "description",
                )
            },
        ),
        ("SEO", {
            "fields": SeoAdminMixin.seo_fields
        }),
    )
    list_display = ("title", "slug", "parent")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ["title"]

    def get_export_resource_class(self):
        return CategoryResources

    def get_export_formats(self):
        formats = (
            base_formats.YAML,
            base_formats.JSON,
            base_formats.XLS,
            base_formats.XLSX
        )
        return formats

    def get_export_queryset(self, request):
        return super().get_export_queryset(request).only("title", "slug", "parent")


class AttributeForm(forms.ModelForm):
    product = AutoCompleteSelectField("product", required=False, label="Товар")
    value = AutoCompleteSelectField("attribute_value", required=False, label="Значение")


class AttributeInline(AjaxSelectAdminTabularInline):
    model = models.Attribute
    form = AttributeForm
    extra = 0


class AttributeAdmin(AjaxSelectAdmin):
    form = AttributeForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(AttributeAdmin, self).get_form(request, obj, **kwargs)
        autoselect_fields_check_can_add(form, self.model, request.user)
        return form


class NumAttributeForm(forms.ModelForm):
    product = AutoCompleteSelectField("product", required=False, label="Товар")


class NumAttributeInline(AjaxSelectAdminTabularInline):
    model = models.NumAttribute
    form = NumAttributeForm
    extra = 0


class NumAttributeAdmin(AjaxSelectAdmin):
    form = AttributeForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(NumAttributeForm, self).get_form(request, obj, **kwargs)
        autoselect_fields_check_can_add(form, self.model, request.user)
        return form


class ColorInline(admin.TabularInline):
    model = models.Color
    extra = 0


class OptionInline(admin.TabularInline):
    model = models.Option
    extra = 0


class ProductForm(forms.ModelForm):
    category = AutoCompleteSelectField("categories", required=True, label="Категория")
    parent = AutoCompleteSelectField("product", required=False, label="Родитель")
    brand = AutoCompleteSelectField("brand", required=False, label="Производитель")


class ProductGalleryInline(admin.TabularInline):
    model = models.ProductGallery
    extra = 0


class StorageInline(admin.TabularInline):
    model = models.ProductStorageCount
    extra = 0
    exclude = ("option",)


class StorageOptionInline(admin.TabularInline):
    model = models.ProductStorageCount
    extra = 0
    exclude = ("product",)


class ProductPriceInline(admin.TabularInline):
    model = models.ProductPrice
    extra = 0


class OptionPriceInline(admin.TabularInline):
    model = models.OptionPrice
    extra = 0


class ProductAdmin(MPTTModelAdmin, SeoAdminMixin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "active",
                    "unloading_id",
                    "title",
                    "title_upper",
                    "slug",
                    "category",
                    "directions",
                    "parent",
                    "brand",
                    "thumbnail",
                    "rent",
                    "sort",
                )
            },
        ),
        (
            "Основное",
            {
                "fields": (
                    "code",
                    "price",
                    "old_price",
                    "step",
                    "status",
                    "count",
                    "unit",
                    "new",
                    "hit",
                    "sale",
                    "description",
                )
            },
        ),
        ("SEO", {"fields": SeoAdminMixin.seo_fields}),
    )
    list_display = ("title", "category", "active", "new", "hit", "sale")
    list_editable = (
        "active",
        "new",
        "hit",
        "sale",
    )
    list_filter = (
        "active",
        "new",
        "hit",
        "sale",
        "category",
    )
    search_fields = ("title", "title_upper", "code", "slug")
    prepopulated_fields = {"slug": ("title",)}
    form = ProductForm
    inlines = [
        ProductGalleryInline,
        AttributeInline,
        NumAttributeInline,
        OptionInline,
        ColorInline,
        StorageInline,
        ProductPriceInline,
    ]
    actions = ["copy_product"]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("category")

    def copy_product(self, request, queryset):
        for product in queryset:
            attributes = product.product_attrbutes.all()
            num_attributes = product.product_num_attrbutes.all()
            options = product.options.all()
            photos = product.product_gallery.all()
            product.pk = None  # копируем товар и к слагу прибавляем id, сохраняем
            product.slug = product.slug + "-copy"
            try:
                product.save()
            except:
                self.message_user(
                    request, "Товар с таким слагом уже существует", level=messages.ERROR
                )
                return

            for attr in attributes:
                attr.pk = None
                attr.product = product
                attr.save()

            for attr in num_attributes:
                attr.pk = None
                attr.product = product
                attr.save()

            for option in options:
                option.pk = None
                option.product = product
                option.save()

            for photo in photos:
                photo.pk = None
                photo.product = product
                photo.save()

        self.message_user(request, "Товар успешно скопирован", level=messages.SUCCESS)

    copy_product.short_description = "Скопировать выбранные товары"


class OptionAdmin(admin.ModelAdmin):
    list_display = ("title", "product", "count", "active", "price")
    list_filter = ("active",)
    search_fields = ("title",)
    inlines = [StorageOptionInline, OptionPriceInline]


class BrandFileInline(admin.TabularInline):
    model = models.BrandFile
    extra = 0


class BrandAdmin(admin.ModelAdmin):
    list_display = ("title", "sort")
    list_editable = ("sort",)
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "active",
                    "title",
                    "title_upper",
                    "slug",
                    "thumbnail",
                    "text",
                    "text_upper",
                    "link",
                    "sort",
                )
            },
        ),
        ("SEO", {"fields": SeoAdminMixin.seo_fields}),
    )

    inlines = [
        BrandFileInline,
    ]


class StorageAdmin(admin.ModelAdmin):
    list_display = ["__str__", "city"]


class AttrGroupAdmin(admin.ModelAdmin):
    list_display = ["__str__", "show", "show_parent", "show_in_header"]
    list_editable = ["show", "show_parent", "show_in_header"]


class PriceForm(forms.ModelForm):
    product = AutoCompleteSelectField("product", required=True, label="Товар")


class PriceAdmin(admin.ModelAdmin):
    form = PriceForm
    list_display = ["product", "type", "value"]
    search_fields = ("type", "product", "value", "old_value")


admin.site.register(models.ProductStorage, StorageAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Direction)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Option, OptionAdmin)
# admin.site.register(models.Country)
admin.site.register(models.Brand, BrandAdmin)
admin.site.register(models.NumAttribute)
admin.site.register(models.AttributesGroup, AttrGroupAdmin)
admin.site.register(models.AttributeValue)
admin.site.register(models.Attribute, AttributeAdmin)
admin.site.register(models.ColorValue)
admin.site.register(models.Color)
admin.site.register(models.ProductPrice, PriceAdmin)
admin.site.register(models.PriceType)
admin.site.register(models.IndexBlock)
