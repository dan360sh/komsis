from django import template

register = template.Library()

@register.simple_tag
def word(count):
    c2 =  False
    try:
        c1 = int(str(count)[-1])
        c2 = int(str(count)[-2:])
    except:
        c2 = False
    if c2:
        if (c2 >= 10 and c2 <= 20) or c1 == 0:
            return " наименований"
    if c1 == 1:
        return " наименование"
    elif c1 in [2,3,4]:
        return " наименования"
    else:
        return " наименований"