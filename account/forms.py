from django import forms
from django.contrib.auth import get_user_model

from account.models import Customer

User = get_user_model()


class SignUpForm(forms.ModelForm):
    """sign up form"""
    firstname = forms.CharField(max_length=20)
    lastname = forms.CharField(max_length=20)
    mobile = forms.CharField(max_length=12)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email']

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        if Customer.objects.filter(mobile=mobile).exists():
            raise forms.ValidationError("Mobile number already exists")
        return mobile

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another Email, this is already taken')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
