from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from bootstrap_modal_forms.generic import BSModalCreateView
from .models import Task
from calendars.forms import TaskForm
from .functions import (
    getPreviousDay,
    getPreviousMonth,
    getPreviousWeek,
    getNextDay,
    getNextMonth,
    getNextWeek,
    getCurrentWeek,
    getYearList
)
from .exceptions import InvalidMonthNumber, InvalidYearNumber
import calendar, datetime

def home(request):
    return redirect('calendars-month')

def monthly(request, yearArg=-1, monthArg=-1):
    try:
        cal = calendar.Calendar(0) #0 is the default!
        if yearArg == -1 and monthArg == -1:
            today = datetime.date.today()
            year = today.year
            month = today.month
        elif monthArg < 1 or monthArg > 12:
            raise InvalidMonthNumber("{} isn't a valid month number!".format(monthArg))
        else:
            year = yearArg
            month = monthArg
    except InvalidMonthNumber as invalidMonthError:
        messages.warning(request, invalidMonthError)
        today = datetime.date.today()
        year = today.year
        month = today.month
    finally:
        prevMonth = getPreviousMonth(year, month)
        nextMonth = getNextMonth(year, month)

        context = {
            'prevMonth': prevMonth,
            'month': calendar.month_name[month],
            'nextMonth': nextMonth,
            'year': year,
            'monthList': cal.itermonthdates(year, month),
        }

        return render(request, 'calendars/monthly.html', context)

def yearly(request, yearArg=-1):
    try:
        cal = calendar.Calendar(0)
        if yearArg == -1:
            today = datetime.date.today()
            year = today.year
        else:
            year = yearArg
    except InvalidYearNumber as invalidYearError:
        messages.warning(request, invalidYearError)
        today = datetime.date.today()
        year = today.year
    finally:
        yearList = getYearList(year, cal)

        context = {
            'prevYear': year - 1,
            'year': year,
            'nextYear': year + 1,
            'yearList': yearList
        }

        return render(request, 'calendars/yearly.html', context)

def daily(request, yearArg=-1, monthArg=-1, dayArg=-1):
    try:
        if yearArg == -1 and monthArg == -1 and dayArg == -1:
            today = datetime.date.today()
        else:
            today = datetime.date(yearArg, monthArg, dayArg)
    except ValueError as error:
        messages.warning(request, "{}/{}/{} isn't a valid date!".format(yearArg, monthArg, dayArg))
        today = datetime.date.today()
    finally:
        prevDay = getPreviousDay(today)
        nextDay = getNextDay(today)

        context = {
            'prevDay': prevDay,
            'nextDay': nextDay,
            'today': today
        }

        return render(request, 'calendars/daily.html', context)

def weekly(request, yearArg=-1, monthArg=-1, dayArg=-1):
    try:
        cal = calendar.Calendar(0)
        if yearArg == -1 and monthArg == -1 and dayArg == -1:
            today = datetime.date.today()
        else:
            today = datetime.date(yearArg, monthArg, dayArg)
    except ValueError as error:
        messages.warning(request, "{}/{}/{} isn't a valid date!".format(yearArg, monthArg, dayArg))
        today = datetime.date.today()
    finally:
        prevWeek = getPreviousWeek(today)
        nextWeek = getNextWeek(today)
        currentWeek = getCurrentWeek(today, cal)
        
        context = {
            'prevWeek': prevWeek,
            'currentWeek': currentWeek,
            'nextWeek': nextWeek,
        }

        return render(request, 'calendars/weekly.html', context)

class TaskCreateView(LoginRequiredMixin, BSModalCreateView):
    model = Task
    form_class = TaskForm
    success_message = "A new task has been created!"

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return self.request.GET.get('next', '/')

