from django.shortcuts import HttpResponse
from django.urls import reverse, resolve, ResolverMatch
from recipes import views
from recipes.models import Recipe
from .test_recipe_base import RecipeTestBase


class RecipesHomeViewTest(RecipeTestBase):
    def test_recipes_home_view_loads_correct_template(self) -> None:
        response: HttpResponse = self.client.get(
            reverse('recipes:home')
        )

        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_show_no_recipe_found_if_no_recipes(self) -> None:
        response: HttpResponse = self.client.get(
            reverse('recipes:home')
        )

        self.assertIn('No recipe found', response.content.decode('utf-8'))

    def test_recipe_home_status_code_200_OK(self) -> None:
        response: HttpResponse = self.client.get(
            reverse('recipes:home')
        )

        self.assertEqual(response.status_code, 200)

    def test_recipe_home_dont_show_recipes_not_published(self) -> None:
        self.make_recipe(is_published=False)

        response: HttpResponse = self.client.get(
            reverse('recipes:home')
        )
        content: str = response.content.decode('utf-8')

        self.assertIn('No recipe found', content)

    def test_recipe_home_view_is_correct(self) -> None:
        url: ResolverMatch = resolve(
            reverse('recipes:home')
        )
        self.assertIs(url.func, views.home)

    def test_recipe_home_template_loads_recipes(self) -> None:
        recipe: Recipe = self.make_recipe()
        response: HttpResponse = self.client.get(
            reverse('recipes:home')
        )
        response_context_length: int = len(response.context['recipes'])
        response_content: str = response.content.decode('utf-8')

        self.assertEqual(response_context_length, 1)
        self.assertIn(recipe.title, response_content)

    def test_recipe_home_view_returns_a_pagination(self) -> None:
        response = resolve(
            reverse('recipes:home')
        )
        ...
