from django import template
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from ..models import Page

register = template.Library()


@register.simple_tag
def get_page(value):
    try:
        if isinstance(value, str):
            try:
                return Page.objects.get(id=int(value))
            except ValueError:
                return Page.objects.get(Q(title=value) | Q(slug=value))
        elif isinstance(value, int):
            return Page.objects.get(id=value)
        else:
            return False
    except ObjectDoesNotExist:
        return False
