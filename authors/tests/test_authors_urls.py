from django.http import HttpResponse
from django.test import Client, TestCase
from django.urls import reverse


class AuthorsUrlsTest(TestCase):
    def setUp(self) -> None:
        self.client: Client = Client()
        return super().setUp()

    def test_authors_url_register_is_correct(self) -> None:
        url: str = reverse('authors:register')
        self.assertEqual(url, '/authors/register/')

    def test_authors_url_regiter_status_code_200_ok(self) -> None:
        response: HttpResponse = self.client.get(
            reverse('authors:register')
        )

        self.assertEqual(response.status_code, 200)

    def test_authors_url_register_create_is_correct(self) -> None:
        url: str = reverse('authors:register_create')
        self.assertEqual(url, '/authors/register/create/')

    def test_authors_url_load_correct_template(self) -> None:
        url: str = reverse('authors:register')

        response: HttpResponse = self.client.get(url)

        self.assertTemplateUsed(response, 'authors/pages/author.html')
