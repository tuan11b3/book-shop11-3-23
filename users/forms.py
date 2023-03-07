# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from store.models import Customer
from django.conf import settings
from .models import myUser
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




