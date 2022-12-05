from django.shortcuts import HttpResponse
from django.urls import reverse, resolve, ResolverMatch
from recipes import views
from recipes.models import Recipe
from .test_recipe_base import RecipeTestBase


class RecipesViewsTest(RecipeTestBase):
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

    def test_recipe_details_view_is_correct(self) -> None:
        url: ResolverMatch = resolve(
            reverse('recipes:recipe', kwargs={'id': 1},)
        )
        self.assertIs(url.func, views.recipe)

    def test_recipe_details_return_404_if_no_recipes_found(self) -> None:
        response: HttpResponse = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 10000})
        )

        self.assertEqual(response.status_code, 404)

    def test_recipe_details_dont_loads_recipe_not_published(self) -> None:
        recipe: Recipe = self.make_recipe(is_published=False)

        response: HttpResponse = self.client.get(
            reverse('recipes:recipe', kwargs={
                'id': recipe.id,
            })
        )

        self.assertEqual(response.status_code, 404)

    def test_recipe_details_template_loads_the_correct_recipe(self) -> None:
        needed_title: str = 'Title for test of recipe details'

        self.make_recipe(title=needed_title)

        response: HttpResponse = self.client.get(
            reverse('recipes:recipe', kwargs={
                'id': 1,
            })
        )

        content: str = response.content.decode('utf-8')

        self.assertIn(needed_title, content)

    def test_recipe_category_view_is_correct(self) -> None:
        url: ResolverMatch = resolve(
            reverse('recipes:category', args=(1,))
        )

        self.assertIs(url.func, views.category)

    def test_recipe_category_return_404_if_no_category_found(self) -> None:
        response: HttpResponse = self.client.get(
            reverse('recipes:category', kwargs={'id': 5000})
        )

        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_the_correct_recipe(self) -> None:
        needed_title: str = 'This is a title for the test of category'
        self.make_recipe(title=needed_title)

        response: HttpResponse = self.client.get(
            reverse('recipes:category', kwargs={'id': 1})
        )

        content: str = response.content.decode('utf-8')

        self.assertIn(needed_title, content)

    def test_recipe_category_dont_load_recipe_not_published(self) -> None:
        recipe: Recipe = self.make_recipe(is_published=False)

        response: HttpResponse = self.client.get(
            reverse('recipes:recipe', kwargs={
                'id': recipe.category.id,
            })
        )

        self.assertEqual(response.status_code, 404)

    def test_recipe_view_search_loads_correct_view(self) -> None:
        url: ResolverMatch = resolve(
            reverse('recipes:search')
        )

        self.assertEqual(url.func, views.search)

    def test_recipe_search_loads_correct_template(self) -> None:
        request: ResolverMatch = self.client.get(
            reverse('recipes:search') + '?q=test'
        )

        self.assertTemplateUsed(request, 'recipes/pages/search.html')

    def test_recipe_search_return_404_if_no_search_term(self) -> None:
        url: str = reverse('recipes:search')
        response: HttpResponse = self.client.get(url)

        self.assertEqual(response.status_code, 404)
