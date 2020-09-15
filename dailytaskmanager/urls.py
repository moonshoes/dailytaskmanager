"""dailytaskmanager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as users_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', users_views.RegistrationView.as_view(), name='register'),
    path('login/', users_views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password-reset/', users_views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', users_views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>', users_views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', users_views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('user/<int:pk>/', users_views.UserDetailView.as_view(), name='user-detail'),
    path('user/<int:pk>/update/', users_views.UserUpdateView.as_view(), name='user-update'),
    path('user/<int:pk>/delete/', users_views.UserDeleteView.as_view(), name='user-delete'),
    path('settings/<int:pk>/update/', users_views.UserSettingsUpdateView.as_view(), name='settings-update'),
    path('', include('calendars.urls')),
]
