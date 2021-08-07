from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from cashier.users.models import cashierUser

class UserForm(UserCreationForm):
    class Meta:
        model = cashierUser
        fields = ['username',]

class UserLoginForm(forms.Form):
    user = None
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    def clean_password(self):
        self.user = authenticate(
            username = self.cleaned_data['username'],
            password = self.cleaned_data['password']
        )

        if not self.user:
            raise ValidationError('Sorry the username and password didn\'t match')

    def save(self):
        return self.user