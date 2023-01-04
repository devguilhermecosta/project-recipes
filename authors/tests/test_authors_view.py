from django.http import HttpResponse
from django.test import TestCase
from django.urls import ResolverMatch, resolve, reverse
from authors import views


class AuthorsLoginViewTest(TestCase):
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

    # def test_login_create_user_is_authenticated(self) -> None:
    #     user: dict = {
    #         'first_name': 'adão',
    #         'last_name': 'da silva',
    #         'username': 'adao123',
    #         'email': 'adao@email.com',
    #         'password': 'Adao1234@@',
    #         'password2': 'Adao1234@@',
    #     }

    #     user_data: dict = {
    #         'username': 'adao123',
    #         'password': 'Adao1234@@',
    #     }

    #     response_1: HttpResponse = self.client.post(  # noqa: F841
    #         reverse('authors:register_create'),
    #         data=user,
    #         follow=True,
    #         )

    #     response_2: HttpResponse = self.client.post(  # noqa: F841
    #         reverse('authors:login_create'),
    #         data=user_data,
    #         follow=True,
    #         )

    def test_url_logout_load_correct_view(self) -> None:
        response: ResolverMatch = resolve(
            reverse('authors:logout')
        )

        self.assertEqual(response.func, views.logout_view)
        self.fail(('finalizar os testes de login e logout. '
                   'Para isso é preciso conseguir fazer o login. '
                   'Finalizar também o manual de elaboração '
                   'dos formulários.')
                  )
