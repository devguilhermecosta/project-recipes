from django.shortcuts import HttpResponse
from django.urls import reverse, ResolverMatch
from django.core.paginator import Page
from .test_recipe_base import RecipeTestBase
from recipes.models import Recipe


class RecipesSearchViewTest(RecipeTestBase):
    def test_recipe_search_loads_correct_template(self) -> None:
        search_term: str = '?q=test'
        request: ResolverMatch = self.client.get(
            reverse('recipes:search') + search_term
        )

        self.assertTemplateUsed(request, 'recipes/pages/search.html')

    def test_recipe_search_return_404_if_no_search_term(self) -> None:
        url: str = reverse('recipes:search')
        response: HttpResponse = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_recipe_search_title_is_on_page_and_escaped(self) -> None:
        search_term: str = '?q=test'
        url: str = reverse('recipes:search') + search_term
        response: HttpResponse = self.client.get(url)

        self.assertIn('Buscando por &#x27;test&#x27',
                      response.content.decode('utf-8')
                      )

    def test_recipe_search_can_find_recipe_by_title(self) -> None:
        url: str = reverse('recipes:search')

        title_one: str = 'Receita de bolo de fubá'
        title_two: str = 'Receita de bolo de côco'

        recipe_one: Recipe = self.make_recipe(title=title_one,
                                              slug='one',
                                              author={'username': 'adãosilva'},
                                              )

        recipe_two: Recipe = self.make_recipe(title=title_two,
                                              slug='two',
                                              author={'username': 'adãorosa'},
                                              )

        response_one: HttpResponse = self.client.get(
            url + f"?q={recipe_one.title}"
            )
        response_one_context: Page = response_one.context['recipes']
        response_one_object: list = response_one_context.object_list

        response_two: HttpResponse = self.client.get(
            url + '?q=' + f"{recipe_two.title}"
        )
        response_two_context: Page = response_two.context['recipes']
        response_two_object: list = response_two_context.object_list

        response_three: HttpResponse = self.client.get(
            url + '?q=' + 'receita de qualquer coisa'
        )

        response_both: HttpResponse = self.client.get(
            url + '?q=' + 'Receita de bolo'
        )
        response_both_context: Page = response_both.context['recipes']
        response_both_objects: list = response_both_context.object_list

        self.assertIn(title_one, str(response_one_object))
        self.assertIn(title_two, str(response_two_object))
        self.assertIn('No recipe found',
                      response_three.content.decode('utf-8')
                      )
        self.assertNotIn(title_one, str(response_two_object))
        self.assertNotIn(title_two, str(response_one_object))
        self.assertIn(title_one, str(response_both_objects))
        self.assertIn(title_two, str(response_both_objects))
