# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from store.models import Customer
from django.conf import settings
from .models import myUser
from store.models import Staff
from phonenumber_field.formfields import PhoneNumberField

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = myUser
        fields = UserCreationForm.Meta.fields + ('username',) # new

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = myUser
        fields = UserChangeForm.Meta.fields

class CustomForm(forms.ModelForm):
    class Meta:
        model = Customer
        phone = PhoneNumberField()
        fields = ('email', 'phone')

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        #phone = PhoneNumberField()
        exclude = ['date_joined']




