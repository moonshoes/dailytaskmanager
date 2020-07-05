from django.shortcuts import redirect, render
import calendar
import datetime
import time

def home(request):
    return redirect('calendars-month')

def monthly(request, yearArg=-1, monthArg=-1):
    cal = calendar.Calendar(0) #0 is the default!
    if yearArg and monthArg == -1:
        today = datetime.date.today()
        year = today.year
        month = today.month
    else:
        year = yearArg
        month = monthArg
    
    if month > 1 and month < 12:
        prevMonth = month - 1
        nextMonth = month + 1
    elif month == 1:
        prevMonth = 12
        nextMonth = month + 1
        year = year - 1
    else:
        prevMonth = month + 1
        nextMonth = 1
        year = year + 1

    context = {
        'prevMonth': prevMonth,
        'month': calendar.month_name[month],
        'nextMonth': nextMonth,
        'year': year,
        'monthList': cal.itermonthdates(year, month)
    }
    return render(request, 'calendars/monthly.html', context)

def yearly(request, yearArg=-1):
    cal = calendar.Calendar(0)
    if yearArg == -1:
        today = datetime.date.today()
        year = today.year
    else:
        year = yearArg

    yearList = []
    for x in range(1,13):
        monthinfo = {
            'monthname': calendar.month_name[x],
            'month': cal.itermonthdates(year, x)
        }
        yearList.append(monthinfo)

    context = {
        'prevYear': year - 1,
        'year': year,
        'nextYear': year + 1,
        'yearList': yearList
    }
    return render(request, 'calendars/yearly.html', context)

def daily(request, yearArg=-1, monthArg=-1, dayArg=-1):
    if yearArg == -1 and monthArg == -1 and dayArg == -1:
        today = datetime.date.today()
    else:
        today = datetime.date(yearArg, monthArg, dayArg)
    
    delta = datetime.timedelta(days=1)
    prevDay = today - delta
    nextDay = today + delta

    context = {
        'prevDay': {
                'year': prevDay.year,
                'month': prevDay.month,
                'day': prevDay.day
            },
        'nextDay': {
                'year': nextDay.year,
                'month': nextDay.month,
                'day': nextDay.day
            },
        'today': today
    }

    return render(request, 'calendars/daily.html', context)

def weekly(request, yearArg=-1, monthArg=-1, dayArg=-1):
    cal = calendar.Calendar(0)
    if yearArg == -1 and monthArg == -1 and dayArg == -1:
        today = datetime.date.today()
    else:
        today = datetime.date(yearArg, monthArg, dayArg)

    delta = datetime.timedelta(weeks=1)
    prevWeek = today - delta
    nextWeek = today + delta

    month = cal.monthdatescalendar(today.year, today.month)
    for week in month:
        if today in week:
            currentWeek = week
            firstDay = week[0]
            lastDay = week[6]
    
    context = {
        'prevWeek': {
                'year': prevWeek.year,
                'month': prevWeek.month,
                'day': prevWeek.day
            },
        'currentWeek': {
                'firstDay': firstDay,
                'lastDay': lastDay
            },
        'nextWeek': {
                'year': nextWeek.year,
                'month': nextWeek.month,
                'day': nextWeek.day
            },
        'week': currentWeek
    }

    return render(request, 'calendars/weekly.html', context)