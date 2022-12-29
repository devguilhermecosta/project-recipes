from django import forms
from django.forms import CharField
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from re import compile


def add_placeholder(field: CharField, placeholder_val: str | int) -> None:
    field.widget.attrs['placeholder'] = f'{placeholder_val}'


def add_widget_attr(field: CharField, attr_name: str, attr_value: str) -> None:
    field.widget.attrs[attr_name] = f'{attr_value}'


def strong_password(password: str) -> None:
    regex = compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError(('A senha precisa ter 8 catacteres.'
                               'Pelo menos uma letra maíscula.'
                               'Pelo menos uma letra minúscula.'
                               'Pelo menos um número'
                               ),
                              code='invalid',
                              )


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['first_name'], 'Digite seu nome')
        add_placeholder(self.fields['last_name'], 'Digite seu sobrenome')
        add_placeholder(self.fields['username'], 'Digite seu usuário')
        add_placeholder(self.fields['email'], 'Digite seu e-mail')
        add_placeholder(self.fields['password'], 'Digite a senha')
        add_placeholder(self.fields['password2'], 'Repita a senha')
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

    first_name: CharField = forms.CharField(
        required=True,
        min_length=4,
        error_messages={
            'min_length': 'O campo nome deve ter pelo menos 4 caracteres',
            'required': 'Este campo é obrigatório',
            })

    password = forms.CharField(required=True,
                               label='Senha',
                               help_text='A senha deve ter letras e números',
                               widget=forms.PasswordInput(),
                               error_messages={
                                   'required': 'Este campo é obrigatório',
                               },
                               validators=[strong_password,],
                               )

    password2 = forms.CharField(required=True,
                                label='Confirme a senha',
                                widget=forms.PasswordInput(),
                                error_messages={
                                    'invalid': 'Verifique seus dados',
                                    'required': 'Este campo é obrigatório',
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
        ]

        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
        }

        help_texts = {
            'username': 'Digite um usuário válido',
        }

        error_messages = {
            'last_name': {
                'required': 'Este campo é obrigatório',
            },
            'username': {
                'required': 'Este campo é obrigatório',
            },
            'email': {
                'invalid': 'Digite um e-mail válido',
                'required': 'Este campo é obrigatório',
            },
        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'minha-classe',
                'id': 'first_name',
                'required': 'Campo obrigatório',
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
