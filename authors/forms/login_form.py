from django import forms
from django.forms import CharField


class LoginForm(forms.Form):
    username: CharField = CharField(
        label='Usuário',
        widget=forms.TextInput(attrs={
            'placeholder': 'Digite seu usuário',
        })
    )
    password: forms.PasswordInput = CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Digite sua senha',
        })
    )
