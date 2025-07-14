# Login form
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
class CustomLoginForm(AuthenticationForm):
    """
    Custom login form that inherits from Django's AuthenticationForm.
    """
    username = forms.CharField(
        label='Username',
        max_length=254,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username', 'autofocus': 'autofocus'})
    )
    password = forms.CharField(
        label='Password',
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'})
    )