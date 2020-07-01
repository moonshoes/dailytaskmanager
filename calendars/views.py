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
        year.append(cal.itermonthdates(today.year, x))

    context = {
        'year': year
    }
    return render(request, 'calendars/yearly.html', context)