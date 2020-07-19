from django.db import models
from django.contrib.auth.models import User

class CalendarEntry(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=150)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class Task(CalendarEntry):
    completed = models.BooleanField(default=False)
    date = models.DateField(auto_now=False, auto_now_add=False)

    class Meta:
        db_table = "task"

    def __str__(self):
        return self.name

class Event(CalendarEntry):
    location = models.CharField(max_length=100)
    startDate = models.DateTimeField(auto_now=False, auto_now_add=False)
    endDate = models.DateTimeField(auto_now=False, auto_now_add=False)