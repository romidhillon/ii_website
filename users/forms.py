from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from traitlets import All


class SignUpForm(UserCreationForm):
    class Meta:
        model =  User
        fields = ['username', 'email', 'password1', 'password2']
        
class SignInForm(AuthenticationForm):
    class Meta:
        model =  User
        fields = ['username', 'password1']
        

