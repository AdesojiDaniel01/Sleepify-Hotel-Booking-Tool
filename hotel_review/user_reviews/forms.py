from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review  # Use the Review model
        fields = ['name', 'rating', 'comment']  # Fields to include in the form
