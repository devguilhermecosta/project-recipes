from django import forms
from django.forms import CharField
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from re import compile


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

    first_name: CharField = forms.CharField(
        min_length=4,
        max_length=128,
        label='Nome',
        widget=forms.TextInput(attrs={
            'placeholder': 'Digite seu nome',
            'class': 'minha-classe',
            'id': 'first_name',
        }),
        error_messages={
            'min_length': 'O campo nome deve ter pelo menos 4 caracteres',
            'max_length': 'O campo nome deve ter 128 caracteres ou menos',
            'required': 'O campo nome é obrigatório',
            })

    last_name: CharField = forms.CharField(
        label='Sobrenome',
        min_length=4,
        max_length=128,
        widget=forms.TextInput(attrs={
            'placeholder': 'Digite seu sobrenome',
        }),
        error_messages={
            'required': 'O campo sobrenome é obrigatório',
            'min_length': 'O campo sobrenome deve ter pelo menos 4 caracteres',
            'max_length': 'O campo sobrenome deve ter 128 caracteres ou menos',
        },
    )

    username: CharField = forms.CharField(
        label='Usuário',
        min_length=4,
        max_length=128,
        widget=forms.TextInput(attrs={
            'placeholder': 'Digite seu usuário',
        }),
        error_messages={
            'required': 'O campo usuário é obrigatório',
            'min_length': 'O campo usuário deve ter pelo menos 4 caracteres',
            'max_length': 'O campo usuário deve ter 128 caracteres ou menos',
        },
        help_text='Digite um usuário válido',
    )

    email: CharField = forms.CharField(
        label='Endereço de email',
        widget=forms.EmailInput(attrs={
            'placeholder': 'Digite seu e-mail',
        }),
        error_messages={
            'invalid': 'Digite um e-mail válido',
            'required': 'Este campo é obrigatório',
        },
    )

    password = forms.CharField(label='Senha',
                               min_length=8,
                               max_length=128,
                               help_text='A senha deve ter letras e números',
                               widget=forms.PasswordInput(attrs={
                                   'placeholder': 'Digite a senha',
                                   }),
                               error_messages={
                                   'required': 'O campo senha é obrigatório',
                                   'min_length': 'A senha deve ter pelo menos 8 caracteres',  # noqa: E501
                                   'max_length': 'O campo senha deve ter 128 caracteres ou menos',  # noqa: E501
                               },
                               validators=[strong_password,],
                               )

    password2 = forms.CharField(label='Confirme a senha',
                                min_length=8,
                                max_length=128,
                                widget=forms.PasswordInput(attrs={
                                    'placeholder': 'Repita a senha',
                                    }),
                                error_messages={
                                    'invalid': 'Verifique seus dados',
                                    'required': 'O campo repita a senha é obrigatório',  # noqa: E501
                                    'min_length': 'A senha deve ter pelo menos 8 caracteres',  # noqa: E501
                                    'max_length': 'O campo senha deve ter 128 caracteres ou menos',  # noqa: E501
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

    def clean_email(self) -> CharField | ValidationError:
        email: CharField = self.cleaned_data.get('email', '')  # pega os dados do input de e-mail  # noqa: E501
        exists: bool = User.objects.filter(email=email).exists()  # verifica se o e-mail já existe  # noqa: E501

        if exists:  # se o email já existir um ValidationError é levantado
            raise ValidationError('E-mail ja cadastrado.',
                                  code='invalid',
                                  )

        return email

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
