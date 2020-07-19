from django import forms
from calendars.models import Task
from bootstrap_modal_forms.forms import BSModalModelForm
from tempus_dominus.widgets import DatePicker

class TaskForm(BSModalModelForm):
    class Meta:
        model = Task
        fields = ('name', 'description', 'date')
        widgets = {
            'description': forms.Textarea(attrs={'cols': 10, 'rows': 2}),
            'date': DatePicker,
        }