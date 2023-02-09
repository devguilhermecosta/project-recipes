from django.test import TestCase
from django.http import HttpResponse
from django.urls import reverse, resolve, ResolverMatch
from recipes import views


class TheoryTests(TestCase):
    def test_theory_url_is_correct(self) -> None:
        response: HttpResponse = reverse(
            'recipes:theory'
        )

        self.assertEqual(response, '/recipes/theory/')

    def test_theory_load_correc_view(self) -> None:
        url: str = reverse('recipes:theory')

        response: ResolverMatch = resolve(url)

        self.assertEqual(response.func, views.theory)

    def test_theory_view_load_correct_template(self) -> None:
        url: str = reverse('recipes:theory')

        response: HttpResponse = self.client.get(url)

        self.assertTemplateUsed(response, 'recipes/pages/theory.html')
