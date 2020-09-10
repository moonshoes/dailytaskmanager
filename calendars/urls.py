from django.urls import path, include
from calendars import views

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
    path('task/new/', views.TaskCreateView.as_view(), name='task-create'),
    path('tasks/', views.UnfinishedTasksListView.as_view(), name='unfinished-tasks'),
    path('task/<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),
    path('task/<int:pk>/update/', views.TaskUpdateView.as_view(), name='task-update'),
    path('task/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task-delete'),
    path('task/<int:pk>/toggle-complete/', views.toggleCompleteTask, name='toggle-complete-task'),

    #Events
    path('event/new/', views.EventCreateView.as_view(), name='event-create'),
    path('events/', views.FutureEventsListView.as_view(), name='future-events'),
    path('event/<int:pk>/', views.EventDetailView.as_view(), name='event-detail'),
    path('event/<int:pk>/update/', views.EventUpdateView.as_view(), name='event-update'),
    path('event/<int:pk>/delete/', views.EventDeleteView.as_view(), name='event-delete'),

    #Habits
    path('habits/', views.HabitListView.as_view(), name='list-habits'),
    path('habit/<int:pk>/', views.HabitDetailView.as_view(), name='habit-detail'),
    path('habit/<int:pk>/delete/', views.HabitDeleteView.as_view(), name='habit-delete'),
    path('habit/new/', views.HabitCreateView.as_view(), name='habit-create'),
    path('habit/<int:pk>/update/', views.HabitUpdateView.as_view(), name='habit-update'),
    path('habit/<int:pk>/toggle-complete/', views.toggleCompleteHabit, name='toggle-complete-habit'),
    path('habit/set-previous-complete/', views.CompleteEarlierDaysHabit.as_view(), name='complete-previous-habit'),
    path('habit/<int:pk>/year-streak/<int:yearArg>', views.habitYearStreak, name='habit-year-streak'),
    path('reward/new/', views.RewardCreateView.as_view(), name='reward-create'),
    path('unlocked-rewards/', views.UnlockedRewardListView.as_view(), name='list-unlocked-rewards'),
    path('reward/unlocked/<int:pk>/delete/', views.UnlockedRewardDeleteView.as_view(), name='unlocked-reward-delete'),
    path('reward/<int:pk>/delete/', views.RewardDeleteView.as_view(), name='reward-delete'),
    path('reward/<int:pk>/update/', views.RewardUpdateView.as_view(), name='reward-update'),
]