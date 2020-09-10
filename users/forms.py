from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import login, password_validation
from .models import UserSettings
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm
from tempus_dominus.widgets import DatePicker, DateTimePicker

class CustomRegistrationForm(PopRequestMixin, CreateUpdateAjaxMixin, UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password1', 'password2']
        labels = {
            'first_name': 'Name'
        }
    
    def save(self, commit=True):
        if not self.request.is_ajax():
            user = super(CreateUpdateAjaxMixin, self).save(commit=commit)
            login(self.request, user)
        else:
            user = super(CreateUpdateAjaxMixin, self).save(commit=False)
        return user

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
    
class UserUpdateForm(BSModalModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']
        labels = {
            'first_name': 'Name'
        }

class UserSettingsForm(BSModalModelForm):
    class Meta:
        model = UserSettings
        fields = ['landingPage', 'firstWeekday']
        labels = {
            'landingPage': 'Home page',
            'firstWeekday': 'First day of the week'
        }
        widgets = {
            'landingPage': forms.Select(
                choices=[
                    ('month', 'Monthly overview'),
                    ('year', 'Yearly overview'),
                    ('week', 'Weekly overview'),
                    ('day', 'Daily overview')
                ]
            ),
            'firstWeekday': forms.Select(
                choices=[
                    (0, 'Monday'),
                    (1, 'Tuesday'),
                    (2, 'Wednesday'),
                    (3, 'Thursday'),
                    (4, 'Friday'),
                    (5, 'Saturday'),
                    (6, 'Sunday')
                ]
            )
        }