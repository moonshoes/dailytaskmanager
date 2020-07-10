import calendar, datetime
from datetime import date
from .exceptions import InvalidMonthNumber, InvalidYearNumber

def getPreviousMonth(year, month):
    if month > 1 and month <= 12:
        month = month - 1
    elif month == 1:
        month = 12
        year = year - 1
    else:
        raise InvalidMonthNumber("{:d} isn't a valid month!".format(month))
    
    return {'year': year, 'month': month}

def getNextMonth(year, month):
    if month >= 1 and month < 12:
        month = month + 1
    elif month == 12:
        month = 1
        year = year + 1
    else:
        raise InvalidMonthNumber("{:d} isn't a valid month!".format(month))
    
    return {'year': year, 'month': month}

def getYearList(year, userCalendar):
    yearList = []
    if year < 0:
        raise InvalidYearNumber("{:d} isn't a valid year!".format(month))

    for x in range(1,13):
        monthinfo = {
            'monthname': calendar.month_name[x],
            'month': userCalendar.itermonthdates(year, x)
        }
        yearList.append(monthinfo)

    return yearList

def getPreviousDay(today):
    if not isinstance(today, date):
        raise TypeError("{} is not a date!".format(today))
    delta = datetime.timedelta(days=1)
    prevDay = today - delta

    return {'year': prevDay.year, 'month': prevDay.month, 'day': prevDay.day}

def getNextDay(today):
    if not isinstance(today, date):
        raise TypeError("{} is not a date!".format(today))
    delta = datetime.timedelta(days=1)
    nextDay = today + delta

    return {'year': nextDay.year, 'month': nextDay.month, 'day': nextDay.day}

def getPreviousWeek(today):
    if not isinstance(today, date):
        raise TypeError("{} is not a date!".format(today))
    delta = datetime.timedelta(weeks=1)
    prevWeek = today - delta

    return {'year': prevWeek.year, 'month': prevWeek.month, 'day': prevWeek.day}

def getNextWeek(today):
    if not isinstance(today, date):
        raise TypeError("{} is not a date!".format(today))
    delta = datetime.timedelta(weeks=1)
    nextWeek = today + delta

    return {'year': nextWeek.year, 'month': nextWeek.month, 'day': nextWeek.day}

def getCurrentWeek(today, userCalendar):
    if not isinstance(today, date):
        raise TypeError("{} is not a date!".format(today))
    if not isinstance(userCalendar, calendar.Calendar):
        raise TypeError("{} is not a calendar!".format(userCalendar))
    month = userCalendar.monthdatescalendar(today.year, today.month)
    for week in month:
        if today in week:
            currentWeek = week
            firstDay = week[0]
            lastDay = week[6]
            break
    
    return {'weekDaysList': week, 'firstWeekDay': firstDay, 'lastWeekDay': lastDay}