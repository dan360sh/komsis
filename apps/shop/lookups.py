from ajax_select import register, LookupChannel

from apps.account.models import Account
from apps.catalog.models import Product


@register('account')
class AccountLookupChannel(LookupChannel):
    model = Account

    def get_query(self, q, request):
        return self.model.objects.filter(user__username__icontains=q)[:10]

    def format_item_display(self, obj):
        return u"<span class='tag'>%s</span>" % obj.user.username[0:20]


@register('product')
class ProductLookupChannel(LookupChannel):
    model = Product

    def get_query(self, q, request):
        return self.model.objects.filter(title__icontains=q)[:10]

    def format_item_display(self, obj):
        return u"<span class='tag'>%s</span>" % obj.title[0:20]
