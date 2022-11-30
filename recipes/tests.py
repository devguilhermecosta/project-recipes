from django.test import TestCase
from django.urls import reverse, resolve, ResolverMatch
from . import views


class RecipesURLsTest(TestCase):
    def test_url_recipe_home_is_correct(self) -> None:
        url: str = reverse('recipes:home')
        self.assertEqual(url, '/')

    def test_url_recipe_category_is_correct(self) -> None:
        url: str = reverse('recipes:category', kwargs={'id': 1})
        self.assertEqual(url, '/recipe/category/1/')

    def test_url_recipe_details_is_correct(self) -> None:
        url: str = reverse('recipes:recipe', kwargs={'id': 1})
        self.assertEqual(url, '/recipe/1/')


class RecipesViewsTest(TestCase):
    def test_recipe_home_view_is_correct(self) -> None:
        view: ResolverMatch = resolve(
            reverse('recipes:home')
        )
        self.assertIs(view.func, views.home)

    def test_recipe_details_view_is_correct(self) -> None:
        view: ResolverMatch = resolve(
            reverse('recipes:recipe', kwargs={'id': 1},)
        )
        self.assertIs(view.func, views.recipe)

    def test_recipe_category_view_is_correct(self) -> None:
        view: ResolverMatch = resolve(
            reverse('recipes:category', args=(1,))
        )

        self.assertIs(view.func, views.category)
