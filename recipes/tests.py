from django.test import TestCase
from django.urls import reverse


class RecipesURLsTest(TestCase):
    def test_url_recipe_home_is_correct(self):
        home_url: str = reverse('recipes:home')  # type: ignore
        self.assertEqual(home_url, '/')
