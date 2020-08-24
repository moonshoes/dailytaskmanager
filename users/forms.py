from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from bootstrap_modal_forms.forms import BSModalModelForm
from tempus_dominus.widgets import DatePicker, DateTimePicker

class CustomRegistrationForm(PopRequestMixin, CreateUpdateAjaxMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
    
class UserUpdateForm(BSModalModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(BSModalModelForm):
    birthdate = forms.DateField(input_formats=['%d/%m/%Y'],
        label='Birthday',
        widget=DatePicker(
                options={
                    'format': 'DD/MM/YYYY'
                },
                attrs={
                'append': 'fa fa-calendar',
                'icon-toggle': True,
            }))
    
    class Meta:
        model = Profile 
        fields = ['name', 'birthdate']