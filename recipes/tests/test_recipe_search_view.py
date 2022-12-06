from django.shortcuts import HttpResponse
from django.urls import reverse, ResolverMatch
from .test_recipe_base import RecipeTestBase


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
