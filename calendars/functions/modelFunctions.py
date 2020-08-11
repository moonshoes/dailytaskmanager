from calendars.models import Task, Habit

#Tasks
def getDailyTasks(day, user):
    return Task.objects.filter(
                creator=user,
                date=day,
            )

def getWeeklyTasks(week, user):
    taskList = []
    for day in week.get('weekDaysList'):
        taskList.append(Task.objects.filter(
            creator=user,
            date=day
        ))
    print(taskList)
    return taskList


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
