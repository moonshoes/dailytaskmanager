from django import forms
import datetime
from calendars.models import Task, Event, Habit, Reward
from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm
from tempus_dominus.widgets import DatePicker, DateTimePicker

class TaskForm(BSModalModelForm):
    date = forms.DateField(input_formats=['%d/%m/%Y'],
        widget=DatePicker(
                options={
                    'format': 'DD/MM/YYYY'
                },
                attrs={
                'append': 'fa fa-calendar',
                'icon-toggle': True,
            }))
    class Meta:
        model = Task
        fields = ('name', 'description', 'date')
        widgets = {
            'description': forms.Textarea(attrs={'cols': 10, 'rows': 2})
        }

class EventForm(BSModalModelForm):
    startDate = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'],
        label='Start date',
        widget=DateTimePicker(
                options={
                    'format': 'DD/MM/YYYY HH:mm'
                },
                attrs={
                    'append': 'fa fa-calendar',
                    'icon-toggle': True,
            }))
    endDate = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'],
        label='End date',
        widget=DateTimePicker(
                options={
                    'format': 'DD/MM/YYYY HH:mm'
                },
                attrs={
                    'append': 'fa fa-calendar',
                    'icon-toggle': True,
            }))
    class Meta:
        model = Event
        fields = ('name', 'description', 'location', 'startDate', 'endDate')
        widgets = {
            'description': forms.Textarea(attrs={'cols': 10, 'rows': 2})
        }

    def clean(self):
        super().clean()
        startDate = self.cleaned_data.get("startDate")
        endDate = self.cleaned_data.get("endDate")

        if startDate is not None and endDate is not None and startDate > endDate:
            msg = "Start date cannot begin after end date."
            self.add_error('startDate', msg)
            self.add_error('endDate', msg)

class HabitForm(BSModalModelForm):
    frequencyChoice = forms.CharField(label="Frequency",
        widget=forms.RadioSelect(
            choices=[
                ('daily', 'Daily'),
                ('personalised', 'Personalised')
            ])
    )
    personalisedFrequency = forms.CharField(
        required=False,
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'form-check-input',
            },
            choices=[
                ('monday', 'M'),
                ('tuesday', 'Tu'),
                ('wednesday', 'W'),
                ('thursday', 'Th'),
                ('friday', 'F'),
                ('saturday', 'Sa'),
                ('sunday', 'Su')
        ])
    )

    class Meta:
        model = Habit
        fields = ('name', 'description', 'iconColor')
        labels = {
            'iconColor': 'Display color'
        }
        widgets = {
            'description': forms.Textarea(attrs={'cols': 10, 'rows': 2})
        }

    def __init__(self, *args, **kwargs):
        super(HabitForm, self).__init__(*args, **kwargs)
        if Habit.objects.all().filter(pk=self.instance.pk).exists():
            habit = Habit.objects.get(pk=self.instance.pk)
            frequency = habit.frequency()
            if frequency == "Every day":
                self.fields['frequencyChoice'].initial = 'daily'
            else:
                initialChoices = []

                if habit.monday:
                    initialChoices.append('monday')
                if habit.tuesday:
                    initialChoices.append('tuesday')
                if habit.wednesday:
                    initialChoices.append('wednesday')
                if habit.thursday:
                    initialChoices.append('thursday')
                if habit.friday:
                    initialChoices.append('friday')
                if habit.saturday:
                    initialChoices.append('saturday')
                if habit.sunday:
                    initialChoices.append('sunday')

                self.fields['frequencyChoice'].initial = 'personalised'
                self.fields['personalisedFrequency'].initial = initialChoices
    
    def clean(self):
        super().clean()
        frequencyChoice = self.cleaned_data.get("frequencyChoice")
        personalisedFrequency = self.cleaned_data.get("personalisedFrequency")

        if frequencyChoice == "personalised":
            if not personalisedFrequency:
                msg = "At least one day should be selected."
                self.add_error('personalisedFrequency', msg)
            else:
                print(personalisedFrequency)

class PreviousCompletedHabitDaysForm(BSModalForm):
    dates = forms.CharField()
    
    def __init__(self, *args, **kwargs):
        self.disabledDates = kwargs.pop('disabledDays')
        print(self.disabledDates)
        self.maxDate = kwargs.pop('maxDate')
        print(self.maxDate)
        super(PreviousCompletedHabitDaysForm, self).__init__(*args, **kwargs)

        self.fields['dates'].widget = DatePicker(
                options={
                    'format': 'DD/MM/YYYY',
                    'allowMultidate': True,
                    'multidateSeparator': ',',
                    'daysOfWeekDisabled': self.disabledDates,
                    # 'maxDate': self.maxDate.isoformat()
                    # With maxDate set it doesn't disable any days?
                },
                attrs={
                    'append': 'fa fa-calendar',
                    'icon-toggle': True,
            })

    def addPreviousDates(self, habit):
        self.clean()
        cleaned_dates = self.cleaned_data.get("dates")
        try:
            habit.completeEarlierDays(cleaned_dates)
        except (IndexError, ValueError, TypeError) as error:
            self.add_error('dates', error)

class RewardForm(BSModalModelForm):
    class Meta:
        model = Reward
        fields = ['days', 'description']
        labels = {
            'days': 'Unlock reward after this many consecutive days'
        }
        widgets = {
            'description': forms.Textarea(attrs={'cols': 10, 'rows': 2})
        }
