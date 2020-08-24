from django.shortcuts import render
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from bootstrap_modal_forms.generic import (
    BSModalCreateView, 
    BSModalLoginView,
    BSModalReadView,
    BSModalUpdateView
)
from users.forms import (
    CustomRegistrationForm, 
    CustomAuthenticationForm,
    UserUpdateForm,
    ProfileUpdateForm
)
from .models import Profile

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
        return self.request.GET.get('next', '/')

class ProfileDetailView(LoginRequiredMixin, BSModalReadView):
    model = Profile 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        next = self.request.GET.get('next', '/')
        context['next'] = next
        return context

class ProfileUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    success_message = "Your profile has been updated!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userForm = UserUpdateForm(instance=self.request.user)
        context['userForm'] = userForm
        return context

    def get_success_url(self):
        return self.request.GET.get('next', '/')