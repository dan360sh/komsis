from django import template
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from ..models import Category, Post

register = template.Library()


@register.simple_tag
def get_category(search):
    try:
        if isinstance(search, str):
            try:
                return Category.objects.get(id=int(search))
            except ValueError:
                return Category.objects.get(Q(title=search) | Q(slug=search))
        elif isinstance(search, int):
            return Category.objects.get(id=search)
        else:
            return False
    except ObjectDoesNotExist:
        return False


@register.simple_tag(takes_context=True)
def get_posts(context, **kwargs):
    try:
        try:
            count = kwargs['count']
        except KeyError:
            count = False

        try:
            category = kwargs['category']
        except KeyError:
            try:
                category = context['object']['category']
            except KeyError:
                category = False

        if category:
            query = Post.objects.filter(category=category)
        else:
            query = Post.objects.all()

        if count:
            return query[:count]
        return query
    except ObjectDoesNotExist:
        return False
