from django import forms

from account.models import Customer


class SignUpForm(forms.Form):
    """sign up form"""
    firstname = forms.CharField(max_length=20)
    lastname = forms.CharField(max_length=20)
    phone_number = forms.CharField(max_length=12)
    email = forms.EmailField()
    password = forms.CharField(max_length=30, widget=forms.PasswordInput)
