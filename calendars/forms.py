from django import forms
import datetime
from calendars.models import Task, Event, Habit
from bootstrap_modal_forms.forms import BSModalModelForm
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
            'iconColor': 'Icon'
        }
        widgets = {
            'description': forms.Textarea(attrs={'cols': 10, 'rows': 2}),
            'iconColor': forms.RadioSelect(
                choices=[
                    ('#ff0000', 'red'), #red
                    ('#00cc00', 'green'), #green
                    ('#0066ff', 'blue'), #blue
                    ('#ffff00', 'yellow')]) #yellow
        }
    
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
