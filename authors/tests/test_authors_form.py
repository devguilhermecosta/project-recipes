from unittest import TestCase
from django.forms import ModelForm
from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from django.http import HttpResponse
from authors.forms import RegisterForm
from parameterized import parameterized


class RegisterFormAuthorsUnitTest(TestCase):
    @parameterized.expand([
        ('first_name', 'Digite seu nome'),
        ('last_name', 'Digite seu sobrenome'),
        ('username', 'Digite seu usuário'),
        ('email', 'Digite seu e-mail'),
        ('password', 'Digite a senha'),
        ('password2', 'Repita a senha'),
    ])
    def test_fields_placeholder_is_correct(self, field, placeholder) -> None:
        form: ModelForm = RegisterForm()
        current_placeholder: str = form[field].field.widget.attrs['placeholder']  # noqa: E501
        self.assertEqual(placeholder, current_placeholder)

    @parameterized.expand([
        ('username', 'Digite um usuário válido'),
        ('password', 'A senha deve ter letras e números'),
    ])
    def test_fields_help_text_is_correct(self, field, help_text) -> None:
        form: ModelForm = RegisterForm()
        current: str = form[field].help_text
        self.assertEqual(current, help_text)

    @parameterized.expand([
        ('first_name', 'Nome'),
        ('last_name', 'Sobrenome'),
        ('username', 'Usuário'),
        ('email', 'Endereço de email'),
        ('password', 'Senha'),
        ('password2', 'Confirme a senha'),
    ])
    def test_fields_label_is_correct(self, field, label) -> None:
        form: ModelForm = RegisterForm()
        current: str = form[field].label
        self.assertEqual(current, label)


class RegisterFormAuthorsIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs) -> None:
        self.form_data = {
            'first_name': 'first name',
            'last_name': 'last name',
            'username': 'username',
            'email': 'email@email.com',
            'password': 'Password123',
            'password2': 'Password123',
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('first_name', 'Este campo é obrigatório'),
        ('last_name', 'Este campo é obrigatório'),
        ('username', 'Este campo é obrigatório'),
        ('email', 'Este campo é obrigatório'),
        ('password', 'Este campo é obrigatório'),
        ('password2', 'Este campo é obrigatório'),
    ])
    def test_fields_cannot_be_empty(self, field, message) -> None:
        self.form_data[field] = ''
        url: str = reverse('authors:create')
        response: HttpResponse = self.client.post(url, data=self.form_data, follow=True)  # noqa: E501

        self.assertIn(message, response.content.decode('utf-8'))
        # self.assertIn(message, response.context['form'].errors.get(field))

    @parameterized.expand([
        ('first_name', 4, 'O campo nome deve ter pelo menos 4 caracteres'),
        ('last_name', 4, 'O campo sobrenome deve ter pelo menos 4 caracteres'),
        ('username', 4, 'O campo usuário deve ter pelo menos 4 caracteres'),
        ('password', 8, 'A senha deve ter pelo menos 8 caracteres'),
        ('password2', 8, 'A senha deve ter pelo menos 8 caracteres'),
    ])
    def test_fields_min_length(self, field, min_length, message) -> None:
        self.form_data[field] = 'a' * (min_length - 1)
        url: str = reverse('authors:create')
        response: HttpResponse = self.client.post(url, data=self.form_data, follow=True)  # noqa: E501

        self.assertIn(message, response.content.decode('utf-8'))

    @parameterized.expand([
        ('first_name', 128, 'O campo nome deve ter 128 caracteres ou menos'),
        ('last_name', 128, 'O campo sobrenome deve ter 128 caracteres ou menos'),  # noqa: E501
        ('username', 128, 'O campo usuário deve ter 128 caracteres ou menos'),
        ('password', 128, 'O campo senha deve ter 128 caracteres ou menos'),
        ('password2', 128, 'O campo senha deve ter 128 caracteres ou menos'),
    ])
    def test_fields_max_length(self, field, max_length, message) -> None:
        self.form_data[field] = 'a' * (max_length + 1)
        url: str = reverse('authors:create')
        response: HttpResponse = self.client.post(url, data=self.form_data, follow=True)  # noqa: E501

        self.assertIn(message, response.context['form'].errors.get(field))
