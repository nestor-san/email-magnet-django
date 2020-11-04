from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import DetailSearch

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class DetailSearchForm(ModelForm):
    class Meta:
        model = DetailSearch
        fields = ['domain', 'first_name', 'middle_name', 'last_name']

