from django.contrib.auth.models import User
from django.http import HttpResponse
from django.test import TestCase
from django.urls import ResolverMatch, resolve, reverse

from authors import views


class AuthorsLoginViewTest(TestCase):
    def setUp(self) -> None:
        self.user: User = User.objects.create_user(username='adao123',
                                                   email='email@email.com',
                                                   password='Adao1234@@',
                                                   )
        self.user.save()

        self.user_data: dict = {
            'username': 'adao123',
            'password': 'Adao1234@@',
        }
        return super().setUp()

    def test_url_register_load_correct_view(self) -> None:
        url: ResolverMatch = resolve(
            reverse('authors:register')
        )
        self.assertEqual(url.func, views.register_view)

    def test_url_register_load_correct_template(self) -> None:
        url: str = reverse('authors:register')
        response: HttpResponse = self.client.get(url)

        self.assertTemplateUsed(response, 'authors/pages/author.html')

    def test_url_register_create_load_correct_view(self) -> None:
        url: ResolverMatch = resolve(
            reverse('authors:register_create')
        )
        self.assertEqual(url.func, views.register_create)

    def test_url_login_load_correc_view(self) -> None:
        response: ResolverMatch = resolve(
            reverse('authors:login')
        )

        self.assertEqual(response.func, views.login_view)

    def test_url_login_load_correct_template(self) -> None:
        url: str = reverse('authors:login')

        response: HttpResponse = self.client.get(url)

        self.assertTemplateUsed(response, 'authors/pages/login.html')

    def test_url_login_create_load_correct_view(self) -> None:
        response: ResolverMatch = resolve(
            reverse('authors:login_create')
        )

        self.assertEqual(response.func, views.login_create)

    def test_login_create_user_is_authenticated(self) -> None:
        response: HttpResponse = self.client.post(
            reverse('authors:login_create'),
            data=self.user_data,
            follow=True,
        )
        response_content: str = response.content.decode('utf-8')

        self.assertIn('Login realizado com sucesso', response_content)
        self.assertIn('Você está logado como adao123', response_content)
        self.assertIn('Clique aqui para sair', response_content)

    def test_login_create_user_is_not_authenticated(self) -> None:
        self.user_data.update({
            'password': '123456',
        })

        response: HttpResponse = self.client.post(
            reverse('authors:login_create'),
            data=self.user_data,
            follow=True,
        )

        response_content: str = response.content.decode('utf-8')

        self.assertIn('Usuário ou senha inválidos.', response_content)

    def test_url_logout_load_correct_view(self) -> None:
        response: ResolverMatch = resolve(
            reverse('authors:logout')
        )

        self.assertEqual(response.func, views.logout_view)

    def test_url_logout_ok(self) -> None:
        url_login: str = reverse('authors:login_create')
        url_logout: str = reverse('authors:logout')

        self.client.post(
            url_login,
            data=self.user_data,
            follow=True
        )

        response_logout: HttpResponse = self.client.post(
            url_logout,
            data=self.user_data,
            follow=True
        )
        response_content: str = response_logout.content.decode('utf-8')

        self.assertIn('Logout realizado com sucesso', response_content)


class AuthorsLogoutViewTest(TestCase):
    def setUp(self) -> None:
        User.objects.create_user(username='gui', password='123')
        self.client.login(username='gui', password='123')

        return super().setUp()

    def test_logout_message_error_if_method_get(self) -> None:
        response: HttpResponse = self.client.get(
            reverse('authors:logout'),
            follow=True,
        )

        self.assertIn(
            'Invalid request',
            response.content.decode('utf-8'),
        )

    def test_logout_message_error_if_invalid_credentials(self) -> None:
        response: HttpResponse = self.client.post(
            reverse('authors:logout'),
            follow=True,
            data={
                'username': 'other_user',
            }
        )

        self.assertIn(
            'Invalid credentials',
            response.content.decode('utf-8'),
        )

    def test_logout_message_succes_if_correct_data(self) -> None:
        response: HttpResponse = self.client.post(
            reverse('authors:logout'),
            follow=True,
            data={
                'username': 'gui',
            }
        )

        self.assertIn(
            'Logout realizado com sucesso',
            response.content.decode('utf-8'),
        )
