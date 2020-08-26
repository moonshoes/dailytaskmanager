from django.db import models
from django.contrib.auth.models import User

class CalendarEntry(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=150, null=True, blank=True)
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

    def toggleCompleted(self):
        self.completed = not self.completed
        self.save()

class Event(CalendarEntry):
    location = models.CharField(max_length=100, null=True, blank=True)
    startDate = models.DateTimeField(auto_now=False, auto_now_add=False)
    endDate = models.DateTimeField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.name

class Habit(CalendarEntry):
    creationDate = models.DateField(auto_now_add=True)
    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    saturday = models.BooleanField(default=False)
    sunday = models.BooleanField(default=False)

    iconColor = models.CharField(max_length=7)

    def __str__(self):
        return self.name
    
    def frequency(self):
        frequency = ""

        if (self.monday and self.tuesday and self.wednesday and self.thursday 
            and self.friday and self.saturday and self.sunday):
            frequency = "Every day"
        else:
            if self.monday:
                frequency = frequency + "Mon, "
            if self.tuesday:
                frequency = frequency + "Tues, "
            if self.wednesday:
                frequency = frequency + "Wed, "
            if self.thursday:
                frequency = frequency + "Thurs, "
            if self.friday:
                frequency = frequency + "Fri, "
            if self.saturday:
                frequency = frequency + "Sat, "
            if self.sunday:
                frequency = frequency + "Sun"
            
            lengthF = len(frequency)
            if lengthF != 0 and frequency[lengthF-1] == " ":
                frequency = frequency[:lengthF-2]
            
        return frequency