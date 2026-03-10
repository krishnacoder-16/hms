from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from doctors.models import Availability
import datetime

class AvailabilityForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    start_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'})
    )
    end_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'})
    )

    class Meta:
        model = Availability
        fields = ['date', 'start_time', 'end_time']

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date and date < timezone.now().date():
            raise ValidationError("You cannot create an availability slot in the past.")
        return date

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time:
            if start_time >= end_time:
                raise ValidationError("Start time must be before end time.")
            
        return cleaned_data
