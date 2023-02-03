from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse


class AuthorsUrlsTest(TestCase):
    def test_authors_url_register_is_correct(self) -> None:
        url: str = reverse('authors:register')
        self.assertEqual(url, '/authors/register/')

    def test_authors_url_regiter_status_code_200_ok(self) -> None:
        response: HttpResponse = self.client.get(
            reverse('authors:register')
        )

        self.assertEqual(response.status_code, 200)

    def test_authors_url_status_code_404_if_method_get(self) -> None:
        url: str = reverse('authors:register_create')
        response: HttpResponse = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_authors_url_register_create_is_correct(self) -> None:
        url: str = reverse('authors:register_create')
        self.assertEqual(url, '/authors/register/create/')

    def test_authors_url_login_status_code_200_ok(self) -> None:
        url: str = reverse('authors:login')

        response: HttpResponse = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_authors_login_create_is_correct(self) -> None:
        url: str = reverse('authors:login_create')

        self.assertEqual(url, '/authors/login/create/')

    def test_authors_login_create_status_code_200_if_method_post(self) -> None:
        url: str = reverse('authors:login_create')
        data: dict = {'username': 'guilherme', 'password': 'Gui123456'}
        response: HttpResponse = self.client.post(url, data=data, follow=True)

        self.assertEqual(response.status_code, 200)

    def test_authors_logout_is_correct(self) -> None:
        url: str = reverse('authors:logout')

        self.assertEqual(url, '/authors/logout/')
