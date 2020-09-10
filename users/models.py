from django.db import models
from django.contrib.auth.models import User


class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    landingPage = models.CharField(max_length=10, default="month")
    firstWeekday = models.IntegerField(default=0)

    def __str__(self):
        return '{} settings'.format(self.user)