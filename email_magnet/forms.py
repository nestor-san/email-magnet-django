from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import DetailSearch

class RegisterForm(UserCreationForm):
    """
    Create a new register form to include the email field
    """
    #Create email field as an EmailField
    email = forms.EmailField()

    #Define the user and the fields for the form
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class DetailSearchForm(ModelForm):
    """
    Form to create a DetailSearchInstance
    """
    class Meta:
        model = DetailSearch
        fields = ['domain', 'first_name', 'middle_name', 'last_name']



