from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from traitlets import All
from .models import Profile , Post


class SignUpForm(UserCreationForm):
    class Meta:
        model =  User
        fields = ['username', 'email', 'password1', 'password2']
        
class SignInForm(AuthenticationForm):
    class Meta:
        model =  User
        fields = ['username', 'password1']
        
class EditUserForm(forms.ModelForm):
    class Meta:
        model = User 
        fields = ('first_name', 'last_name', 'email')

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile 
        fields = ('image',)

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'image', 'caption')
