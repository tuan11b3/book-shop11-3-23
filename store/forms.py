from django import forms

from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        exclude = ['responded', 'staff_id', 'custom_id']

