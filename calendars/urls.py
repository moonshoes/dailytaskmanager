from django.urls import path, include
from .views import TaskCreateView, EventCreateView
from . import views

urlpatterns = [
    path('', views.home, name='calendars-home'),
    path('year/', views.yearly, name='calendars-year'),
    path('year/<int:yearArg>/', views.yearly, name='calendars-year'),
    path('month/', views.monthly, name='calendars-month'),
    path('month/<int:yearArg>/<int:monthArg>/', views.monthly, name='calendars-month'),
    path('week/', views.weekly, name='calendars-week'),
    path('week/<int:yearArg>/<int:monthArg>/<int:dayArg>/', views.weekly, name='calendars-week'),
    path('day/', views.daily, name='calendars-day'),
    path('day/<int:yearArg>/<int:monthArg>/<int:dayArg>/', views.daily, name='calendars-day'),
    path('task/new/', TaskCreateView.as_view(), name='task-create'),
    path('event/new/', EventCreateView.as_view(), name='event-create'),
]