from django import forms
from django.forms import CharField
from django.contrib.auth.models import User


def add_placeholder(field: CharField, placeholder_val: str | int) -> None:
    field.widget.attrs['placeholder'] = f'{placeholder_val}'


def add_widget_attr(field: CharField, attr_name: str, attr_value: str) -> None:
    field.widget.attrs[attr_name] = f'{attr_value}'


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        add_widget_attr(self.fields['password'], 'placeholder', 'Digite sua senha')  # noqa: E501

    password2 = forms.CharField(required=True,
                                label='Confirme a senha',
                                min_length=3,
                                max_length=5,
                                widget=forms.PasswordInput(attrs={
                                    'placeholder': 'Repita a senha',
                                    }),
                                error_messages={
                                    'invalid': 'Verifique seus dados',
                                    'min_length': 'Deve ter pelo menos 3 caracteres',  # noqa: E501
                                },
                                )

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
            'password': 'A senha deve ter letras e números',
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
        }
