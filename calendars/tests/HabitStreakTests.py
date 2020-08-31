from django.test import TestCase
from calendars.models import Habit, HabitStreak
from django.contrib.auth.models import User

class TestFrequencyToArray(TestCase):
    def setUpData(cls):
        cls.user = User.objects.create()
        cls.habit = Habit.objects.create(name="testHabit", )