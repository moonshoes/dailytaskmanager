import calendar, datetime
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import ListView
from bootstrap_modal_forms.generic import (
    BSModalCreateView, 
    BSModalReadView,
    BSModalUpdateView,
    BSModalDeleteView,
    BSModalFormView
)
from calendars.models import Task, Event, Habit, Reward, RewardStreak
from users.models import UserSettings
from calendars.forms import TaskForm, EventForm, HabitForm, RewardForm, PreviousCompletedHabitDaysForm
from calendars.functions import modelFunctions, calendarFunctions


# ==============
# CALENDAR VIEWS
# ==============
def home(request):
    if not request.user.is_anonymous:
        landing = request.user.usersettings.landingPage
        if landing == "year":
            return redirect('calendars-year')
        elif landing == "month":
            return redirect('calendars-month')
        elif landing == "week":
            return redirect('calendars-week')
        elif landing == "day":
            return redirect('calendars-day')
    else:
        return redirect('calendars-month')

def monthly(request, yearArg=-1, monthArg=-1):
    try:
        if not request.user.is_anonymous:
            cal = calendar.Calendar(request.user.usersettings.firstWeekday)
        else:
            cal = calendar.Calendar(0) #0 is the default, which is a monday!
        today = datetime.date.today()
        if yearArg == -1 and monthArg == -1:
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
        monthList = cal.itermonthdates(year, month)

        context = {
            'today': datetime.date.today(),
            'prevMonth': calendarFunctions.getPreviousMonth(year, month),
            'month': calendar.month_name[month],
            'nextMonth': calendarFunctions.getNextMonth(year, month),
            'year': year,
            'monthList': monthList
        }

        if not request.user.is_anonymous:
            context['monthList'] = modelFunctions.getMonthlyEntries(monthList, request.user)
            context['dailyTasks'] = modelFunctions.getDailyTasks(today, request.user)
            context['dailyHabits'] = modelFunctions.getDailyHabits(today, request.user)

        return render(request, 'calendars/monthly.html', context)

def yearly(request, yearArg=-1):
    try:
        if not request.user.is_anonymous:
            cal = calendar.Calendar(request.user.usersettings.firstWeekday)
        else:
            cal = calendar.Calendar(0) #0 is the default, which is a monday!
        today = datetime.date.today()
        if yearArg == -1:
            year = today.year
        else:
            year = yearArg
        yearList = calendarFunctions.getYearList(year, cal)
    except InvalidYearNumber as invalidYearError:
        messages.warning(request, invalidYearError)
        today = datetime.date.today()
        year = today.year
        yearList = calendarFunctions.getYearList(year, cal)
    finally:
        context = {
            'today': datetime.date.today(),
            'prevYear': year - 1,
            'year': year,
            'nextYear': year + 1,
            'yearList': yearList
        }

        if not request.user.is_anonymous:
            context['dailyTasks'] = modelFunctions.getDailyTasks(today, request.user)
            context['dailyHabits'] = modelFunctions.getDailyHabits(today, request.user)

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
        prevDay = calendarFunctions.getPreviousDay(today)
        nextDay = calendarFunctions.getNextDay(today)

        context = {
            'prevDay': prevDay,
            'nextDay': nextDay,
            'currentDay': today,
            'today': datetime.date.today()
        }

        if not request.user.is_anonymous:
            context['dailyTasks'] = modelFunctions.getDailyTasks(datetime.date.today(), request.user)
            context['dayTasks'] = modelFunctions.getDailyTasks(today, request.user)
            context['dailyHabits'] = modelFunctions.getDailyHabits(datetime.date.today(), request.user)
            context['dailyEvents'] = modelFunctions.getDailyEvents(today, request.user)
            context['dayHabits'] = modelFunctions.getDailyHabits(today, request.user)

        return render(request, 'calendars/daily.html', context)

def weekly(request, yearArg=-1, monthArg=-1, dayArg=-1):
    try:
        if not request.user.is_anonymous:
            cal = calendar.Calendar(request.user.usersettings.firstWeekday)
        else:
            cal = calendar.Calendar(0) #0 is the default, which is a monday!
        if yearArg == -1 and monthArg == -1 and dayArg == -1:
            today = datetime.date.today()
        else:
            today = datetime.date(yearArg, monthArg, dayArg)
    except ValueError as error:
        messages.warning(request, "{}/{}/{} isn't a valid date!".format(yearArg, monthArg, dayArg))
        today = datetime.date.today()
    finally:
        prevWeek = calendarFunctions.getPreviousWeek(today)
        nextWeek = calendarFunctions.getNextWeek(today)
        currentWeek = calendarFunctions.getCurrentWeek(today, cal)
        
        context = {
            'today': datetime.date.today(),
            'prevWeek': prevWeek,
            'currentWeek': currentWeek,
            'nextWeek': nextWeek
        }

        if not request.user.is_anonymous:
            context['dailyTasks'] = modelFunctions.getDailyTasks(datetime.date.today(), request.user)
            context['dailyHabits'] = modelFunctions.getDailyHabits(datetime.date.today(), request.user)
            context['currentWeek'] = modelFunctions.getWeeklyEntries(currentWeek, request.user)

        return render(request, 'calendars/weekly.html', context)

# This is for both clicking on a day in the yearly overview
# and clicking on the "read more" button in the monthly overview
def DayDetailView(request, yearArg, monthArg, dayArg):
    try:
        today = datetime.date(yearArg, monthArg, dayArg)
    except ValueError as error:
        messages.warning(request, "{}/{}/{} isn't a valid date!".format(yearArg, monthArg, dayArg))
        today = datetime.date.today()
    finally:
        next = request.GET.get('next', '/')

        context = {
            'next': next,
            'today': today,
            'tasks': modelFunctions.getDailyTasks(today, request.user),
            'events': Event.objects.filter(
                    startDate__date__lte=today,
                    endDate__date__gte=today,
                    creator=request.user
                ),
            'habits': modelFunctions.getDailyHabits(today, request.user)
        }

        return render(request, 'calendars/day.html', context)

# This is used for the overflow in the weekly overview
def HourDetailView(request, yearArg, monthArg, dayArg, hourArg):
    try:
        hour = datetime.datetime(yearArg, monthArg, dayArg, hourArg)
    except ValueError as error:
        messages.warning(request, "{}/{}/{} {}:00 isn't a valid datetime!".format(yearArg, monthArg, dayArg, hourArg))
        hour = datetime.now()
    finally:
        next = request.GET.get('next', '/')

        context = {
            'next': next,
            'hour': hour,
            'nextHour': calendarFunctions.getNextHour(hour),
            'events': Event.objects.filter(
                    startDate__lte=hour,
                    endDate__gt=hour,
                    creator=request.user
                )
        }

        return render(request, 'calendars/hour.html', context)


# ==========
# TASK VIEWS
# ==========
class TaskCreateView(LoginRequiredMixin, BSModalCreateView):
    model = Task
    form_class = TaskForm
    success_message = "A new task has been created!"

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return self.request.GET.get('next', '/')

class UnfinishedTasksListView(LoginRequiredMixin, ListView):
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

        context['dailyTasks'] = modelFunctions.getDailyTasks(today, user)
        context['dailyHabits'] = modelFunctions.getDailyHabits(today, user)
        return context

class TaskDetailView(LoginRequiredMixin, BSModalReadView):
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        next = self.request.GET.get('next', '/')

        context['next'] = next
        return context

class TaskUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Task
    form_class = TaskForm
    success_message = "The task has been updated!"

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return self.request.GET.get('next', '/')

class TaskDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Task
    success_message = "The task has been deleted!"
    template_name = 'calendars/confirm_delete.html'

    def get_success_url(self):
        return self.request.GET.get('next', '/')

def toggleCompleteTask(request, pk):
    task = modelFunctions.findTask(pk)
    modelFunctions.toggleCompleteTask(task)
    next = request.GET.get('next', '/')
    return redirect(next)


# ===========
# EVENT VIEWS
# ===========
class EventCreateView(LoginRequiredMixin, BSModalCreateView):
    model = Event
    form_class = EventForm
    success_message = "A new event has been created!"

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return self.request.GET.get('next', '/')

class FutureEventsListView(LoginRequiredMixin, ListView):
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

        context['dailyTasks'] = modelFunctions.getDailyTasks(today, user)
        context['dailyHabits'] = modelFunctions.getDailyHabits(today, user)
        context['today'] = datetime.date.today()
        context['now'] = now
        return context

class EventDetailView(LoginRequiredMixin, BSModalReadView):
    model = Event

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        now = timezone.now
        next = self.request.GET.get('next', '/')

        context['now'] = now
        context['next'] = next
        return context

class EventUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Event
    form_class = EventForm
    success_message = "The event has been updated!"

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return self.request.GET.get('next', '/')

class EventDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Event
    success_message = "The event has been deleted!"
    template_name = 'calendars/confirm_delete.html'

    def get_success_url(self):
        return self.request.GET.get('next', '/')


# ===========
# HABIT VIEWS
# ===========
class HabitListView(LoginRequiredMixin, ListView):
    model = Habit
    context_object_name = 'habits'

    def get_queryset(self):
        user = self.request.user
        return Habit.objects.filter(creator=user).order_by('creationDate')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        today = datetime.date.today()
        user = self.request.user

        context['dailyTasks'] = modelFunctions.getDailyTasks(today, user)
        context['dailyHabits'] = modelFunctions.getDailyHabits(today, user)
        context['today'] = today
        context['currentYear'] = today.year
        return context

class HabitDetailView(LoginRequiredMixin, BSModalReadView):
    model = Habit

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['next'] = self.request.GET.get('next', '/')
        context['today'] = datetime.date.today()
        return context

class HabitDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Habit
    success_message = "The habit has been deleted!"
    template_name = 'calendars/confirm_delete.html'

    def get_success_url(self):
        return self.request.GET.get('next', '/')

class HabitCreateView(LoginRequiredMixin, BSModalCreateView):
    model = Habit
    form_class = HabitForm
    success_message = "A new habit has been created!"

    def form_valid(self, form):
        form.instance.creator = self.request.user

        if self.request.POST.get("frequencyChoice") == "daily":
            form.instance.monday = True
            form.instance.tuesday = True
            form.instance.wednesday = True
            form.instance.thursday = True
            form.instance.friday = True
            form.instance.saturday = True
            form.instance.sunday = True
        else:
            for day in self.request.POST.getlist("personalisedFrequency"):
                if day == 'monday':
                    form.instance.monday = True
                elif day == 'tuesday':
                    form.instance.tuesday = True
                elif day == 'wednesday':
                    form.instance.wednesday = True
                elif day == 'thursday':
                    form.instance.thursday = True
                elif day == 'friday':
                    form.instance.friday = True
                elif day == 'saturday':
                    form.instance.saturday = True
                elif day == 'sunday':
                    form.instance.sunday = True

        return super().form_valid(form)

    def get_success_url(self):
        return self.request.GET.get('next', '/')

class HabitUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Habit
    form_class = HabitForm
    success_message = "The habit has been updated!"

    def form_valid(self, form):
        form.instance.creator = self.request.user

        if self.request.POST.get("frequencyChoice") == "daily":
            form.instance.monday = True
            form.instance.tuesday = True
            form.instance.wednesday = True
            form.instance.thursday = True
            form.instance.friday = True
            form.instance.saturday = True
            form.instance.sunday = True
        else:
            #Set all days to false in case of an update from every day -> personalised days
            #Or in the case of unticking a day and selecting others instead!
            form.instance.monday = False
            form.instance.tuesday = False
            form.instance.wednesday = False
            form.instance.thursday = False
            form.instance.friday = False
            form.instance.saturday = False
            form.instance.sunday = False
            for day in self.request.POST.getlist("personalisedFrequency"):
                if day == 'monday':
                    form.instance.monday = True
                elif day == 'tuesday':
                    form.instance.tuesday = True
                elif day == 'wednesday':
                    form.instance.wednesday = True
                elif day == 'thursday':
                    form.instance.thursday = True
                elif day == 'friday':
                    form.instance.friday = True
                elif day == 'saturday':
                    form.instance.saturday = True
                elif day == 'sunday':
                    form.instance.sunday = True

        return super().form_valid(form)
    
    def get_success_url(self):
        return self.request.GET.get('next', '/')

def toggleCompleteHabit(request, pk):
    habit = modelFunctions.findHabit(pk)
    today = datetime.date.today()
    modelFunctions.toggleCompleteHabit(habit, today)

    next = request.GET.get('next', '/')
    return redirect(next)

class CompleteEarlierDaysHabit(BSModalFormView):
    form_class = PreviousCompletedHabitDaysForm
    template_name = 'calendars/habit_previous_days_form.html'
    success_message = "You've successfully added previous completed dates!"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.habit = modelFunctions.findHabit(self.request.GET.get('habit'))
        kwargs['disabledDays'] = modelFunctions.getDisabledDaysHabit(self.habit)
        kwargs['maxDate'] = datetime.date.today()
        return kwargs

    def form_valid(self, form):
        form.addPreviousDates(self.habit)
        return super().form_valid(form)

    def get_success_url(self):
       return self.request.GET.get('next', '/')

def habitYearStreak(request, pk, yearArg=-1):
    try:
        cal = calendar.Calendar(0)
        today = datetime.date.today()
        if yearArg == -1:
            year = today.year
        else:
            year = yearArg
        yearList = calendarFunctions.getYearList(year, cal)
    except InvalidYearNumber as invalidYearError:
        messages.warning(request, invalidYearError)
        today = datetime.date.today()
        year = today.year
        yearList = calendarFunctions.getYearList(year, cal)
    finally:
        habit = modelFunctions.findHabit(pk)
        context = {
            'today': datetime.date.today(),
            'prevYear': year - 1,
            'year': year,
            'nextYear': year + 1,
            'yearList': yearList,
            'dailyTasks': modelFunctions.getDailyTasks(today, request.user),
            'dailyHabits': modelFunctions.getDailyHabits(today, request.user),
            'yearStreak': modelFunctions.getYearStreak(habit, year),
            'habit': habit
        }

        return render(request, 'calendars/habit_year_streak.html', context)

# ============
# REWARD VIEWS
# ============
class RewardCreateView(BSModalCreateView):
    model = Reward
    form_class = RewardForm
    success_message = "You've added a new reward!"

    def form_valid(self, form):
        habit = modelFunctions.findHabit(self.request.GET.get('habit'))
        form.instance.habit = habit
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['habit'] = modelFunctions.findHabit(self.request.GET.get('habit'))
        return context

    def get_success_url(self):
        return self.request.GET.get('next', '/')

class UnlockedRewardListView(LoginRequiredMixin, ListView):
    model = RewardStreak
    context_object_name = 'rewards'
    template_name = 'calendars/unlocked_rewards.html'

    def get_queryset(self):
        user = self.request.user
        habits = Habit.objects.filter(creator=user)
        rewards = []
        for habit in habits:
            for reward in list(habit.getRewards()):
                rewards.append(reward)
        return RewardStreak.objects.filter(reward__in=rewards, unlocked=True).order_by('unlockDate')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        today = datetime.date.today()
        user = self.request.user

        context['dailyTasks'] = modelFunctions.getDailyTasks(today, user)
        context['dailyHabits'] = modelFunctions.getDailyHabits(today, user)
        context['today'] = today
        return context

# Deletes unlocked rewards because a user has cashed them in
class UnlockedRewardDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = RewardStreak
    success_message = "Your reward has been completed!"
    template_name = 'calendars/confirm_reward_done.html'

    def get_success_url(self):
        return self.request.GET.get('next', '/')

# Deletes entire reward, prevents user from unlocking new rewards for it
class RewardDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Reward
    success_message = "Your reward has been deleted!"
    template_name = 'calendars/confirm_delete.html'

    def get_success_url(self):
        return self.request.GET.get('next', '/')