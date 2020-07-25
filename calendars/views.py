import calendar, datetime

from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import ListView

from bootstrap_modal_forms.generic import BSModalCreateView, BSModalReadView

from calendars.models import Task, Event
from calendars.forms import TaskForm, EventForm
from calendars.functions.calendarFunctions import (
    getPreviousDay,
    getPreviousMonth,
    getPreviousWeek,
    getNextDay,
    getNextMonth,
    getNextWeek,
    getCurrentWeek,
    getYearList
)
from calendars.functions.modelFunctions import getDailyTasks
from calendars.exceptions import InvalidMonthNumber, InvalidYearNumber


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
            'dailyTasks': getDailyTasks(today, request.user)
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
            'yearList': yearList,
            'dailyTasks': getDailyTasks(today, request.user)
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
            'today': today,
            'dailyTasks': getDailyTasks(today, request.user)
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
            'dailyTasks': getDailyTasks(today, request.user)
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

class EventCreateView(LoginRequiredMixin, BSModalCreateView):
    model = Event
    form_class = EventForm
    success_message = "A new event has been created!"

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return self.request.GET.get('next', '/')

class UnfinishedTasksListView(ListView):
    model = Task
    template_name = 'calendars/unfinished_tasks.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(creator=user, completed=False).order_by('date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        today = datetime.date.today()
        user = self.request.user

        context['dailyTasks'] = getDailyTasks(today, user)
        return context

class TaskDetailView(BSModalReadView):
    model = Task

class FutureEventsListView(ListView):
    model = Event
    template_name = 'calendars/future_events.html'
    context_object_name = 'events'

    def get_queryset(self):
        user = self.request.user
        now = timezone.now()
        
        return Event.objects.filter(creator=user, endDate__gte=now).order_by('startDate')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        today = datetime.date.today()
        now = timezone.now
        user = self.request.user

        context['dailyTasks'] = getDailyTasks(today, user)
        context['now'] = now
        return context