import re

from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def meta_title(context):
    settings = context['settings']
    meta_template_title = settings.meta_template_title

    # Стандартный заголовок относительно настроек сайта
    if settings.meta_title == '' or not settings.meta_title:
        general_title = settings.name
    else:
        general_title = settings.meta_title

    try:
        obj = context['object']
        if meta_template_title == '' or not meta_template_title:
            try:
                if obj.meta_title == '' or not obj.meta_title:
                    return obj.title
                else:
                    return obj.meta_title
            except AttributeError:
                return obj.title
        else:
            try:
                if not obj.meta_title == '' and obj.meta_title:
                    return obj.meta_title
            except AttributeError:
                pass
            try:
                title = obj.title
            except AttributeError:
                title = str(obj)
            meta_template_title = re.sub(
                r'\|\|site\|\|', settings.name, meta_template_title)
            meta_template_title = re.sub(
                r'\|\|object\|\|', title, meta_template_title)
            return meta_template_title
    except KeyError:
        return general_title


@register.simple_tag(takes_context=True)
def meta_description(context):
    settings = context['settings']
    meta_template_description = settings.meta_template_description
    try:
        obj = context['object']
        if not meta_template_description:
            try:
                if not obj.meta_description:
                    meta_template_description = settings.meta_description
                else:
                    meta_template_description = obj.meta_description
            except AttributeError:
                meta_template_description = settings.meta_description
        else:
            try:
                if obj.meta_description:
                    meta_template_description =  obj.meta_description
            except AttributeError:
                pass
    except KeyError:
        meta_template_description =  settings.meta_description
    meta_template_description = re.sub(
        r'\|\|site\|\|', settings.name, meta_template_description)
    if context.get('object'):
        try:
            general_title = obj.title
        except AttributeError:
            general_title = str(obj)
    else:
        if not settings.meta_title:
            general_title = settings.name
        else:
            general_title = settings.meta_title
    meta_template_description = re.sub(
        r'\|\|object\|\|', general_title, meta_template_description)
    return meta_template_description