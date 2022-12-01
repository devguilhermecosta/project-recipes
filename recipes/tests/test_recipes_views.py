from django.test import TestCase
from django.shortcuts import HttpResponse
from django.urls import reverse, resolve, ResolverMatch
from recipes import views
from recipes.models import Recipe, Category
from django.contrib.auth.models import User


class RecipesViewsTest(TestCase):
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

    def test_recipe_home_view_is_correct(self) -> None:
        view: ResolverMatch = resolve(
            reverse('recipes:home')
        )
        self.assertIs(view.func, views.home)

    def test_recipe_home_template_loads_recipes(self) -> None:
        category: Category = Category.objects.create(name='Categoria')

        author: User = User.objects.create_user(
            first_name='first name',
            last_name='last name',
            username='username',
            password='123456',
            email='username@email.com',
        )

        recipe: Recipe = Recipe.objects.create(
            title='Recipe title',
            description='Recipe Description',
            slug='Recipe Slug',
            preparation_time=30,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='Porções',
            preparation_steps='Preparation Steps',
            is_published=True,
            category=category,
            author=author,
        )

        response: HttpResponse = self.client.get(
            reverse('recipes:home')
        )
        response_context_length: int = len(response.context['recipes'])
        response_content: str = response.content.decode('utf-8')

        self.assertEqual(response_context_length, 1)
        self.assertIn(recipe.title, response_content)
        self.assertIn(recipe.description, response_content)

    def test_recipe_details_view_is_correct(self) -> None:
        view: ResolverMatch = resolve(
            reverse('recipes:recipe', kwargs={'id': 1},)
        )
        self.assertIs(view.func, views.recipe)

    def test_recipe_details_return_404_if_no_recipes_found(self) -> None:
        response: HttpResponse = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 10000})
        )

        self.assertEqual(response.status_code, 404)

    def test_recipe_category_view_is_correct(self) -> None:
        view: ResolverMatch = resolve(
            reverse('recipes:category', args=(1,))
        )

        self.assertIs(view.func, views.category)

    def test_recipe_category_return_404_if_no_category_found(self) -> None:
        response: HttpResponse = self.client.get(
            reverse('recipes:category', kwargs={'id': 5000})
        )

        self.assertEqual(response.status_code, 404)
