from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
        }

        help_texts = {
            'username': 'Digite um usuário válido',
        }

        error_messages = {
            'email': {
                'invalid': 'Digite um e-mail válido',
                'required': 'Este campo é obrigatório',
            },
            'first_name': {
                'min_length': 'Digite no mínimo 5 caracteres',
            },
        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Digite seu nome',
                'class': 'minha-classe',
                'id': 'first_name',
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Digite sua senha',
            }),
        }
