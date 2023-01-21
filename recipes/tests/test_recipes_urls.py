from django.test import TestCase
from django.urls import reverse


class RecipesURLsTest(TestCase):
    def test_url_recipe_home_is_correct(self) -> None:
        url: str = reverse('recipes:home')
        self.assertEqual(url, '/')

    def test_url_recipe_category_is_correct(self) -> None:
        url: str = reverse('recipes:category', kwargs={'category_id': 1})
        self.assertEqual(url, '/recipe/category/1/')

    def test_url_recipe_details_is_correct(self) -> None:
        url: str = reverse('recipes:recipe', kwargs={'pk': 1})
        self.assertEqual(url, '/recipe/1/')

    def test_url_recipe_search_is_correct(self) -> None:
        url: str = reverse('recipes:search')
        self.assertEqual(url, '/recipe/search/')
