from django.shortcuts import redirect, render
import calendar
import datetime
import time

def home(request):
    return redirect('calendars-month')

def monthly(request):
    cal = calendar.Calendar(0) #0 is the default!
    today = datetime.date.today()
    context = {
        'month': cal.itermonthdates(today.year, today.month)
    }
    return render(request, 'calendars/monthly.html', context)

def yearly(request):
    cal = calendar.Calendar(0)
    today = datetime.date.today()

    year = []
    for x in range(1,13):
        monthinfo = {
            'monthname': calendar.month_name[x],
            'month': cal.itermonthdates(today.year, x)
        }
        year.append(monthinfo)

    context = {
        'year': year
    }
    return render(request, 'calendars/yearly.html', context)

def daily(request):
    today = datetime.date.today()
    context = {
        'today': today
    }

    return render(request, 'calendars/daily.html', context)

def weekly(request):
    cal = calendar.Calendar(0)
    today = datetime.date.today()

    month = cal.monthdatescalendar(today.year, today.month)
    for week in month:
        if today in week:
            currentWeek = week
    
    context = {
        'week': currentWeek
    }

    return render(request, 'calendars/weekly.html', context)