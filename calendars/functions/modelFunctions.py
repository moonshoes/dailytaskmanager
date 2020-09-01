from calendars.models import Task, Habit, Event, RewardStreak
from django.db.models import Q

#Tasks
def getDailyTasks(day, user):
    return Task.objects.filter(
                creator=user,
                date=day,
            )

def getWeeklyTasks(week, user):
    taskList = []
    for day in week.get('weekDaysList'):
        taskList.append(getDailyTasks(day, user))
    return taskList

def findTask(pk):
    return Task.objects.get(pk=pk)

def toggleCompleteTask(task):
    task.toggleCompleted()


#Events
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

#Entries (Events, Tasks and Habits)
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

#Habits
def getDailyHabits(day, user):
    #throw error if weekday not >1 or <8
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
    
    return habits

def findHabit(pk):
    return Habit.objects.get(pk=pk)

def toggleCompleteHabit(habit, dateArg):
    habit.toggleCompleteToday(dateArg)

def getDisabledDaysHabit(habit):
    frequencyArray = habit.frequencyToArray()
    disabledDays = []
    for iteration, day in enumerate(frequencyArray):
        if not day:
            if iteration == 6:
                disabledDays.append(0)
            else:
                disabledDays.append(iteration + 1)
    return disabledDays

def getYearStreak(habit, year):
    days = []
    for streak in habit.getStreaks():
        start = streak.startDate
        days.append(start)
        end = streak.endDate
        while start != end:
            start = streak.nextFrequencyDate(start)
            days.append(start)
    return days