from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from .models import UserSettings
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from bootstrap_modal_forms.generic import (
    BSModalCreateView, 
    BSModalLoginView,
    BSModalReadView,
    BSModalUpdateView,
    BSModalDeleteView,
    BSModalFormView
)
from bootstrap_modal_forms.mixins import PassRequestMixin
from django.contrib.messages.views import SuccessMessageMixin
from users.forms import (
    CustomRegistrationForm, 
    CustomAuthenticationForm,
    UserUpdateForm,
    UserSettingsForm
)

class RegistrationView(BSModalCreateView):
    form_class = CustomRegistrationForm
    template_name = 'users/register.html'
    success_message = "Your account has been created!"
    
    def get_success_url(self):
        return self.request.GET.get('next', '/')

class CustomLoginView(BSModalLoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'users/login.html'
    success_message = "Welcome! You've successfully logged in."

    def get_success_url(self):
        return reverse_lazy('calendars-home')

class UserDetailView(LoginRequiredMixin, BSModalReadView):
    model = User
    template_name = 'users/user_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        next = self.request.GET.get('next', '/')
        context['next'] = next
        return context

class UserUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = User
    template_name = 'users/user_form.html'
    form_class = UserUpdateForm
    success_message = "Your user information has been updated!"

    def get_success_url(self):
        return self.request.GET.get('next', '/')

class UserSettingsUpdateView(BSModalUpdateView):
    model = UserSettings
    form_class = UserSettingsForm
    success_message = "Your settings have been saved!"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return self.request.GET.get('next', '/')

class UserDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = User
    success_message = "Thank you for using DailyTaskManager! We're sad to see you go :("
    template_name = 'users/confirm_account_deletion.html'
    success_url = reverse_lazy('calendars-home')