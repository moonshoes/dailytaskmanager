from django.shortcuts import render
import calendar
import datetime
import time

def home(request):
    cal = calendar.Calendar(0)
    today = datetime.date.today()
    context = {
        'month': cal.itermonthdates(today.year, today.month)
    }
    return render(request, 'calendars/monthly.html', context)
