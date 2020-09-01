from django.contrib import admin
from . import models

admin.site.register(models.Task)
admin.site.register(models.Event)
admin.site.register(models.Habit)
admin.site.register(models.HabitStreak)
admin.site.register(models.Reward)
admin.site.register(models.RewardStreak)