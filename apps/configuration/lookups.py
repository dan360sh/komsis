from .utils import HrefModel

from ajax_select import register, LookupChannel


@register('hrefs')
class HrefModelLookup(LookupChannel):
    model = HrefModel

    def get_query(self, q, request):
        values = []
        for href in self.model.objects.all():
            object_link = href.get_object()
            if object_link and object_link.title.lower().find(q.lower()) != -1:
                values.append(href)
        return values
