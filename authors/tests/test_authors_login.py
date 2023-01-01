from django.test import TestCase
from django.urls import reverse, resolve, ResolverMatch
from django.http import HttpResponse
from authors import views


class AuthorsLoginUrlTest(TestCase):
    def test_authors_login_url_is_correct(self) -> None:
        url: str = reverse('authors:login')

        self.assertEqual('/authors/login/', url)

    def test_authors_login_load_correct_view(self) -> None:
        response: ResolverMatch = resolve(
            reverse('authors:login')
        )

        self.assertEqual(response.func, views.login_view)

    def test_authors_login_load_correct_template(self) -> None:
        url: str = reverse('authors:login')

        response: HttpResponse = self.client.get(url)

        self.assertTemplateUsed(response, 'authors/pages/login.html')

    def test_authors_login_create_is_correct(self) -> None:
        url: str = reverse('authors:login_create')

        self.assertEqual('/authors/login/create/', url)

    def test_authors_login_create_load_correct_view(self) -> None:
        response: ResolverMatch = resolve(
            reverse('authors:login_create')
        )

        self.assertEqual(response.func, views.login_create)
