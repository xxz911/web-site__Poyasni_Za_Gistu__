from types import NoneType

from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from datetime import date

from poyasnizagistu import settings
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    captcha = CaptchaField(label='Введите код')
    required_css_class = 'required'
    birthday = forms.DateField(label='День рождения',input_formats=settings.DATE_INPUT_FORMATS, required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'avatar', 'gender', 'birthday')

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) > 20:
            raise ValidationError("Имя пользователя не должно превышать 20 символов")
        return username

    def clean_birthday(self):
        birthday = self.cleaned_data['birthday']
        if birthday:
            today = date.today()
            age = str(today - birthday)
            if int(age.split()[0]) < 5844:
                raise ValidationError("Вы должны быть старше 16 лет")
            return birthday
        else:
            self.birthday = None
            return self.birthday

class ProfileChangeForm(forms.ModelForm):
    avatar = forms.ImageField(label='Аватар', widget=forms.FileInput, required=False)
    required_css_class = 'required'

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'avatar', 'gender', 'birthday')

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) > 20:
            raise ValidationError("Имя пользователя не должно превышать 20 символов")
        return username

    def clean_birthday(self):
        birthday = self.cleaned_data['birthday']
        if birthday:
            today = date.today()
            age = str(today - birthday)
            if int(age.split()[0]) < 5844:
                raise ValidationError("Вы должны быть старше 16 лет")
            return birthday
        else:
            self.birthday = None
            return self.birthday
