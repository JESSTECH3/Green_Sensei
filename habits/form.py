from django import forms
from .models import Habit

class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['category', 'description', 'impact_score']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe your habit'}),
            'impact_score': forms.NumberInput(attrs={'min': 0, 'max': 100}),
        }
