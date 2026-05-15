from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'title',
            'description',
            'category',
            'skills_required',
            'budget_min',
            'budget_max',
            'deadline',
            'is_active'
        ]