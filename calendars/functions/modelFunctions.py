from calendars.models import Task

def getDailyTasks(day, user):
    return Task.objects.filter(
                creator=user,
                date=day,
            )
