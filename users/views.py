from django.shortcuts import render
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalLoginView
from users.forms import CustomRegistrationForm, CustomAuthenticationForm

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

# class CustomLogoutView(LogoutView):
#     messages.success(self.request, "You've been successfully logged out!")
