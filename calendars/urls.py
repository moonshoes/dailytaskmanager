from django.urls import path, include
from .views import (
    TaskCreateView, 
    EventCreateView, 
    UnfinishedTasksListView,
    TaskDetailView,
    FutureEventsListView,
    EventDetailView,
    TaskUpdateView,
    EventUpdateView,
    TaskDeleteView,
    EventDeleteView,
    HabitListView,
    HabitDetailView,
    HabitDeleteView,
    HabitCreateView,
    HabitUpdateView,
    CompleteEarlierDaysHabit
)
from . import views

urlpatterns = [
    #Calendar
    path('', views.home, name='calendars-home'),
    path('year/', views.yearly, name='calendars-year'),
    path('year/<int:yearArg>/', views.yearly, name='calendars-year'),
    path('month/', views.monthly, name='calendars-month'),
    path('month/<int:yearArg>/<int:monthArg>/', views.monthly, name='calendars-month'),
    path('week/', views.weekly, name='calendars-week'),
    path('week/<int:yearArg>/<int:monthArg>/<int:dayArg>/', views.weekly, name='calendars-week'),
    path('day/', views.daily, name='calendars-day'),
    path('day/<int:yearArg>/<int:monthArg>/<int:dayArg>/', views.daily, name='calendars-day'),
    path('day/<int:yearArg>/<int:monthArg>/<int:dayArg>/detail/', views.DayDetailView, name='day-detail'),
    path('hour/<int:yearArg>/<int:monthArg>/<int:dayArg>/<int:hourArg>/detail/', views.HourDetailView, name='hour-detail'),

    #Tasks
    path('task/new/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/', UnfinishedTasksListView.as_view(), name='unfinished-tasks'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('task/<int:pk>/update/', TaskUpdateView.as_view(), name='task-update'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
    path('task/<int:pk>/toggle-complete/', views.toggleCompleteTask, name='toggle-complete-task'),

    #Events
    path('event/new/', EventCreateView.as_view(), name='event-create'),
    path('events/', FutureEventsListView.as_view(), name='future-events'),
    path('event/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('event/<int:pk>/update/', EventUpdateView.as_view(), name='event-update'),
    path('event/<int:pk>/delete/', EventDeleteView.as_view(), name='event-delete'),

    #Habit URLs
    path('habits/', HabitListView.as_view(), name='list-habits'),
    path('habit/<int:pk>/', HabitDetailView.as_view(), name='habit-detail'),
    path('habit/<int:pk>/delete/', HabitDeleteView.as_view(), name='habit-delete'),
    path('habit/new/', HabitCreateView.as_view(), name='habit-create'),
    path('habit/<int:pk>/update/', HabitUpdateView.as_view(), name='habit-update'),
    path('habit/<int:pk>/toggle-complete/', views.toggleCompleteHabit, name='toggle-complete-habit'),
    path('habit/set-previous-complete/', CompleteEarlierDaysHabit.as_view(), name='complete-previous-habit'),
    path('habit/<int:pk>/year-streak/<int:yearArg>', views.habitYearStreak, name='habit-year-streak'),
]