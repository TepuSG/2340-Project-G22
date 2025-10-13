from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'skills', 'location', 'salary', 'is_remote', 'visa_sponsorship']
