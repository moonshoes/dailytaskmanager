from django import template
import datetime, operator, pytz

register = template.Library()

@register.filter(name='range')
def forRange(start, end):
    return range(start, end)

@register.filter()
def hour(value):
    if value == 0 or value == 12:
        remainder = 12
    else:
        remainder = operator.mod(value, 12)

    if value < 12:
        suffix = 'AM'
    else:
        suffix = 'PM'

    return '{:d} {}'.format(remainder, suffix)

@register.filter()
def currentlyHappening(value, arg):
    return value >= arg