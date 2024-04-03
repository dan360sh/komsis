from django import template
from django.db.models import Prefetch
from django.core.exceptions import ObjectDoesNotExist

from ..models import Navigation

register = template.Library()


@register.simple_tag
def get_nav(search):
    try:
        try:
            return (Navigation
            		.objects
            		.get(alias=search)
            		.child
            		.select_related('object_href')
            		.prefetch_related(
            			Prefetch('child', Navigation.objects.select_related('object_href').all())
            			)
            		)
        except ValueError:
            return []
    except ObjectDoesNotExist:
        return []
