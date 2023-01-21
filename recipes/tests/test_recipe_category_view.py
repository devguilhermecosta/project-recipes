from django.shortcuts import HttpResponse
from django.urls import reverse, resolve, ResolverMatch
from recipes import views
from recipes.models import Recipe
from .test_recipe_base import RecipeTestBase


class RecipesCategoryViewTest(RecipeTestBase):
    def test_recipe_category_view_is_correct(self) -> None:
        url: ResolverMatch = resolve(
            reverse('recipes:category', args=(1,))
        )

        self.assertIs(url.func.view_class, views.RecipeCategory)

    def test_recipe_category_return_404_if_no_category_found(self) -> None:
        response: HttpResponse = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 5000})
        )

        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_the_correct_recipe(self) -> None:
        needed_title: str = 'This is a title for the test of category'
        self.make_recipe(title=needed_title)

        response: HttpResponse = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1})
        )

        content: str = response.content.decode('utf-8')

        self.assertIn(needed_title, content)

    def test_recipe_category_dont_load_recipe_not_published(self) -> None:
        recipe: Recipe = self.make_recipe(is_published=False)

        response: HttpResponse = self.client.get(
            reverse('recipes:recipe', kwargs={
                'pk': recipe.category.id,
            })
        )

        self.assertEqual(response.status_code, 404)
