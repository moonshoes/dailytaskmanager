from calendars.models import Task, Habit, Event, RewardStreak
from django.db.models import Q
from datetime import date
from django.contrib.auth.models import User

# Tasks
def getDailyTasks(day, user):
    return Task.objects.filter(
                creator=user,
                date=day,
            )

def findTask(pk):
    return Task.objects.get(pk=pk)

def toggleCompleteTask(task):
    task.toggleCompleted()


# Events
def getDailyEvents(day, user):
    events = {
        'allDay': Event.objects.filter(
            startDate__date__lt=day,
            endDate__date__gt=day,
            creator=user
        ),
        'misc': Event.objects.filter(
            Q(startDate__date=day) |
            Q(endDate__date=day),
            Q(creator=user)
        )
    }
    return events

def getDayEvents(day, user):
    return Event.objects.filter(
                    startDate__date__lte=day,
                    endDate__date__gte=day,
                    creator=user
                )

# Entries (Events, Tasks and Habits)
def getMonthlyEntries(month, user):
    dayEntryList = []
    for day in month:
        dayEntryList.append(
            {
                'day': day,
                'taskList': getDailyTasks(day, user),
                'eventList': Event.objects.filter(
                    startDate__date__lte=day,
                    endDate__date__gte=day,
                    creator=user
                ),
                'habitList': getDailyHabits(day, user)
            }
        )
    return dayEntryList

def getWeeklyEntries(week, user):
    dayEntryList = []
    for day in week.get('weekDaysList'):
        dayEntryList.append(
            {
                'day': day,
                'taskList': getDailyTasks(day, user),
                'eventList': getDailyEvents(day, user),
                'habitList': getDailyHabits(day, user)
            }
        )
    week.update({'weekDaysList': dayEntryList})
    return week

# Habits
def getDailyHabits(day, user):
    if not isinstance(day, date):
        raise TypeError("{} is not a valid date!".format(day))
    if not isinstance(user, User):
        raise TypeError("{} is not a valid user!".format(user))
    weekDay = day.isoweekday()
    habitsUser = Habit.objects.filter(creator=user, creationDate__lte=day)

    if weekDay == 1:
        habits = habitsUser.filter(monday=True)
    elif weekDay == 2:
        habits = habitsUser.filter(tuesday=True)
    elif weekDay == 3:
        habits = habitsUser.filter(wednesday=True)
    elif weekDay == 4:
        habits = habitsUser.filter(thursday=True)
    elif weekDay == 5:
        habits = habitsUser.filter(friday=True)
    elif weekDay == 6:
        habits = habitsUser.filter(saturday=True)
    else:
        habits = habitsUser.filter(sunday=True)
    
    habits = list(habits)

    # In the (unlikely) case that a user adds earlier days than the creation date
    for habit in Habit.objects.filter(creator=user, creationDate__gt=day):
        if earlierCompleted(habit, day):
            habits.append(habit)
    
    return habits

def earlierCompleted(habit, day):
    return habit.completedToday(day)

def findHabit(pk):
    return Habit.objects.get(pk=pk)

def toggleCompleteHabit(habit, dateArg):
    habit.toggleCompleteToday(dateArg)

def getDisabledDaysHabit(habitArg):
    if not isinstance(habitArg, Habit):
        raise TypeError("{} is not a habit!".format(habitArg))
    frequencyArray = habitArg.frequencyToArray()
    disabledDays = []
    for iteration, day in enumerate(frequencyArray):
        if not day:
            if iteration == 6:
                disabledDays.append(0)
            else:
                disabledDays.append(iteration + 1)
    return disabledDays

def getYearStreak(habitArg, year):
    if not isinstance(habitArg, Habit):
        raise TypeError("{} is not a habit!".format(habitArg))
    if not isinstance(year, int):
        raise ValueError("{} is not a valid year!".format(year))
    days = []
    for streak in habitArg.getYearStreaks(year):
        start = streak.startDate
        if start.year == year:
            days.append(start)
        end = streak.endDate
        while start != end:
            start = streak.nextFrequencyDate(start)
            if start.year == year:
                days.append(start)
    return days