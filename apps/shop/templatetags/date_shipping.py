from django import template
from django.utils.timezone import datetime
from datetime import timedelta

register = template.Library()


@register.simple_tag
def date_shipping():
    date_now = datetime.now()
    week_day = date_now.weekday()
    
    if week_day >= 0 and week_day < 4:
        if date_now.hour < 14:
            date = date_now
        else:
            date = date_now + timedelta(days=1)
    elif week_day == 4:
        if date_now.hour < 14:
            date = date_now
        else:
            date = date_now + timedelta(days=3)
    elif week_day == 5:
        date = date_now + timedelta(days=2)
    elif week_day == 6:
        date = date_now + timedelta(days=1)
    else:
        return "??.??.??"
    return date.strftime('%d.%m.%Y')