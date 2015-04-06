from django import template
from django.template.defaultfilters import stringfilter
from topformguide.util import string
from topformguide.util import conversion
from topformguide.util import constants

register = template.Library()


@register.filter
@stringfilter
def fromenum(value):
    return string.constantToHuman(value)


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


@register.filter
def volumetolitres(value, fromunit=constants.CUBIC_CM, precision=1):
    return conversion.convertVolumeToLitres(value, fromunit, precision)