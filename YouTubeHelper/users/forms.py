from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Имя пользователя',
        required=True,
        max_length=150
    )
    password = forms.CharField(
        label='Пароль',
        required=True,
        max_length=128,
        widget=forms.PasswordInput()
    )


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
