from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import UserSettings
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from bootstrap_modal_forms.forms import BSModalModelForm
from tempus_dominus.widgets import DatePicker, DateTimePicker

class CustomRegistrationForm(PopRequestMixin, CreateUpdateAjaxMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
    
class UserUpdateForm(BSModalModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name','email']

class CustomPasswordChangeForm(PopRequestMixin, CreateUpdateAjaxMixin, PasswordChangeForm):
    def save(self, commit=True):
        password = self.cleaned_data['new_password1']
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user

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