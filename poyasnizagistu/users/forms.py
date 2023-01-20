from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    captcha = CaptchaField(label='Введите код')
    required_css_class = 'required'

    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'avatar', 'gender', 'age')

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) > 20:
            raise ValidationError("Имя пользователя не должно превышать 20 символов")
        return username
class ProfileChangeForm(forms.ModelForm):
    avatar = forms.ImageField(label='Аватар', widget=forms.FileInput, required=False)
    required_css_class = 'required'

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'avatar', 'gender', 'age')


