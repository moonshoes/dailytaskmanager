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
    return value > arg

@register.filter()
def habitFrequency(value):
    _params = value.split(',')
    frequency = ""

    if (_params[0] and _params[1] and _params[2] and _params[3] 
        and _params[4] and _params[5] and _params[6]):
        frequency = "Every day"
    else:
        if _params[0]:
            frequency = frequency + "Mon, "
        if _params[1]:
            frequency = frequency + "Tues, "
        if _params[2]:
            frequency = frequency + "Wed, "
        if _params[3]:
            frequency = frequency + "Thurs, "
        if _params[4]:
            frequency = frequency + "Fri, "
        if _params[5]:
            frequency = frequency + "Sat, "
        if _params[6]:
            frequency = frequency + "Sun"
        
    return frequency