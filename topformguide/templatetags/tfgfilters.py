from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def fromenum(value):
    return value.title().replace('_', ' ')


@register.filter
def roundnum(value, precision=2):
    if type(value).__name__ != 'float':
        return "'" + str(value) + "'"

    return round(value, precision)


@register.filter
def checkifint(value):
    if int(value) == value:
        return int(value)
    else:
        return value