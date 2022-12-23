from django.test import TestCase, Client
from django.urls import reverse, resolve, ResolverMatch
from django.http import HttpResponse
from authors import views


class AuthorsUrlsTest(TestCase):
    def setUp(self) -> None:
        self.client: Client = Client()
        return super().setUp()

    def test_authors_url_register_load_correct_view(self) -> None:
        url: ResolverMatch = resolve(
            reverse('authors:register')
        )
        self.assertEqual(url.func, views.register_view)
        ...

    def test_authors_url_register_load_correct_template(self) -> None:
        url: str = reverse('authors:register')
        response: HttpResponse = self.client.get(url)

        self.assertTemplateUsed(response, 'authors/pages/author.html')

    def test_authors_url_register_create_load_correct_view(self) -> None:
        url: ResolverMatch = resolve(
            reverse('authors:create')
            )
        self.assertEqual(url.func, views.register_create)
