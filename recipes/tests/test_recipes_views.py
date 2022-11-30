from django.test import TestCase
from django.urls import reverse, resolve, ResolverMatch
from recipes import views


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
