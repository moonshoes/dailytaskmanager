from calendars.models import Task, Habit, Event
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

#Tasks and events
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
                )
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
                'eventList': getDailyEvents(day, user)
            }
        )
    week.update({'weekDaysList': dayEntryList})
    return week

#Habits
def getDailyHabits(weekDay, user):
    #throw error if weekday not >1 or <8
    habitsUser = Habit.objects.filter(creator=user)

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
