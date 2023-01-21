from django.shortcuts import HttpResponse
from django.urls import reverse, resolve, ResolverMatch
from recipes import views
from recipes.models import Recipe
from .test_recipe_base import RecipeTestBase


class RecipesDetailsViewTest(RecipeTestBase):
    def test_recipe_details_view_is_correct(self) -> None:
        url: ResolverMatch = resolve(
            reverse('recipes:recipe', kwargs={'pk': 1},)
        )
        self.assertIs(url.func.view_class, views.RecipeDetailsView)

    def test_recipe_details_return_404_if_no_recipes_found(self) -> None:
        response: HttpResponse = self.client.get(
            reverse('recipes:recipe', kwargs={'pk': 10000})
        )

        self.assertEqual(response.status_code, 404)

    def test_recipe_details_dont_loads_recipe_not_published(self) -> None:
        recipe: Recipe = self.make_recipe(is_published=False)

        response: HttpResponse = self.client.get(
            reverse('recipes:recipe', kwargs={
                'pk': recipe.id,
            })
        )

        self.assertEqual(response.status_code, 404)

    def test_recipe_details_template_loads_the_correct_recipe(self) -> None:
        needed_title: str = 'Title for test of recipe details'

        self.make_recipe(title=needed_title)

        response: HttpResponse = self.client.get(
            reverse('recipes:recipe', kwargs={
                'pk': 1,
            })
        )

        content: str = response.content.decode('utf-8')

        self.assertIn(needed_title, content)
