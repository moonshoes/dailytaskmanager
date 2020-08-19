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

@register.filter()
def sameDayEvent(start, end):
    return start.day == end.day

@register.filter()
def multipleDayEvent(start, end):
    return start.day != end.day

@register.filter()
def beginningOfMonth(value):
    # print("bm")
    return value == 1

@register.filter()
def beginningOfWeek(value):
    # print("bw")
    return operator.mod(value, 7) == 1

@register.filter()
def isToday(start, day):
    # print("st")
    return start.date() == day

@register.filter()
def compareStartDateHour(date, hour):
    return hour >= date.time().hour

@register.filter()
def compareEndDateHour(date, hour):
    return (hour <= date.time().hour and 
        (hour != date.time().hour or 
            (hour == date.time().hour and
            date.time().minute > 0)))

# @register.filter()
# def columnLine(value):
#     return operator.mod(value, 7)