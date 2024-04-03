from ajax_select import register, LookupChannel

from .models import Category, Product, Brand, AttributeValue


@register('categories')
class CategoriesLookups(LookupChannel):
    model = Category

    def get_query(self, q, request):
        return self.model.objects.filter(title__icontains=q)[:10]

    def format_item_display(self, obj):
        return u"<span class='tag'>%s</span>" % obj.title[0:20]


@register('product')
class ProductLookups(LookupChannel):
    model = Product

    def get_query(self, q, request):
        return self.model.objects.filter(title__icontains=q)[:10]

    def format_item_display(self, obj):
        return u"<span class='tag'>%s</span>" % obj.title[0:20]


@register('brand')
class BrandLookups(LookupChannel):
    model = Brand

    def get_query(self, q, request):
        return self.model.objects.filter(title__icontains=q)[:10]

    def format_item_display(self, obj):
        return u"<span class='tag'>%s</span>" % obj.title[0:20]


@register('attribute_value')
class AttributeValueLookups(LookupChannel):
    model = AttributeValue

    def get_query(self, q, request):
        return self.model.objects.filter(title__icontains=q)[:10]

    def format_item_display(self, obj):
        return u"<span class='tag'>%s</span>" % obj.title[0:30]
