from django import forms
from .models import Recommendation

class RecommendationForm(forms.ModelForm):
    class Meta:
        model = Recommendation
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your recommendation'}),
        }
