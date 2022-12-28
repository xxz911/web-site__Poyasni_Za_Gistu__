from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    captcha = CaptchaField(label='Код')
    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'avatar', 'gender', 'age')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'avatar', 'age')
