from django import forms
from django.forms import CharField
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


def add_placeholder(field: CharField, placeholder_val: str | int) -> None:
    field.widget.attrs['placeholder'] = f'{placeholder_val}'


def add_widget_attr(field: CharField, attr_name: str, attr_value: str) -> None:
    field.widget.attrs[attr_name] = f'{attr_value}'


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    password2 = forms.CharField(required=True,
                                label='Confirme a senha',
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
            'password': {
                'invalid': 'Digite um e-mail válido',
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

    def clean_password(self) -> str:
        data: str = self.cleaned_data.get('password')

        if 'atenção' in data:
            raise ValidationError('Você não pode digitar %(pipoca)s no password',  # noqa: E501
                                  code='invalid',
                                  params={'pipoca': '"atenção"'}
                                  )
        return data

    def clean_first_name(self) -> str:
        data: str = self.cleaned_data.get('first_name')

        if 'guilherme' in data:
            raise ValidationError('Não pode digitar %(value)s no first name',
                                  code='invalid',
                                  params={'value': '"guilherme"'},
                                  )
        return data

    def clean(self) -> None:
        cleaned_data = super().clean()
        password_one = cleaned_data.get('password')
        password_two = cleaned_data.get('password2')

        if password_one != password_two:
            raise ValidationError(
                {'password': ValidationError('%(value)s. As senhas precisam ser iguais',  # noqa: E501
                                             code='invalid',
                                             params={'value': 'ERROR'}),
                 'password2': ValidationError('%(value)s. Senha diferente da senha one.',  # noqa: E501
                                              code='invalid',
                                              params={'value': 'ERROR'}),
                 }
                )
