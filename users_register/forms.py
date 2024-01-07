from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import MyProfile


class RegisterForm(UserCreationForm):
    
    class Meta:
        model = User
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
            }
        fields = ['username', 'email', 'password1', 'password2']
        

class MyProfileForm(forms.ModelForm):
    class Meta:
        model = MyProfile
        fields = ['first_name', 'last_name', 'birthday', 'phone']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Last Name'}),
            'birthday': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Enter Birthday'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone'}),
            }