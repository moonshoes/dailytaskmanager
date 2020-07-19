from django import forms
from calendars.models import Task, Event
from bootstrap_modal_forms.forms import BSModalModelForm
from tempus_dominus.widgets import DatePicker, DateTimePicker

class TaskForm(BSModalModelForm):
    class Meta:
        model = Task
        fields = ('name', 'description', 'date')
        widgets = {
            'description': forms.Textarea(attrs={'cols': 10, 'rows': 2}),
            'date': DatePicker(attrs={
                'append': 'fa fa-calendar',
                'icon-toggle': True,
            }),
        }

class EventForm(BSModalModelForm):
    class Meta:
        model = Event
        fields = ('name', 'description', 'location', 'startDate', 'endDate')
        widgets = {
            'description': forms.Textarea(attrs={'cols': 10, 'rows': 2}),
            'startDate': DateTimePicker(
                options={
                    'extraFormats': True
                },
                attrs={
                'append': 'fa fa-calendar',
                'icon-toggle': True,
            }),
            'endDate': DateTimePicker(attrs={
                'append': 'fa fa-calendar',
                'icon-toggle': True,
            })
        }