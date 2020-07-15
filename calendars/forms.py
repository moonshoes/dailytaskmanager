from django import forms
from calendars.models import Task
from tempus_dominus.widgets import DatePicker

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('name', 'description', 'date')
        widgets = {
            'description': forms.Textarea,
            'date': DatePicker,
        }