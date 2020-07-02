from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='calendars-home'),
    path('month/', views.monthly, name='calendars-month'),
    path('year/', views.yearly, name='calendars-year'),
]