from django.test import Client
from recipes.tests.test_recipe_base import RecipeTestBase
from recipes.models import Recipe
from utils.pagination import make_pagination_range
from django.core.paginator import Page
from django.urls import reverse
from django.http import HttpResponse


class TestRecipePagination(RecipeTestBase):
    def test_make_pagination_range_returns_a_pagination_range(self) -> None:
        pagination: list[int] = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1,
        )['pagination']

        self.assertEqual([1, 2, 3, 4], pagination)

    def test_make_pagination_range_is_static_if_range_less_igual_4(self) -> None:  # noqa: E501
        pagination: list[int] = make_pagination_range(
            page_range=list(range(1, 4)),
            qty_pages=4,
            current_page=1,
        )['pagination']

        self.assertEqual([1, 2, 3], pagination)

    def test_first_range_is_static_if_current_page_is_less_than_middle_page(self) -> None:  # noqa: E501
        pagination_1: list[int] = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1,
        )['pagination']

        self.assertEqual([1, 2, 3, 4], pagination_1)

        pagination_2: list[int] = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=2,
        )['pagination']

        self.assertEqual([1, 2, 3, 4], pagination_2)

        pagination_3: list[int] = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=3,
        )['pagination']

        self.assertEqual([2, 3, 4, 5], pagination_3)

        pagination_4: list[int] = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=4,
        )['pagination']

        self.assertEqual([3, 4, 5, 6], pagination_4)

    def test_make_sure_middle_ranges_are_correct(self) -> None:
        pagination: list[int] = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=10,
        )['pagination']

        self.assertEqual([9, 10, 11, 12], pagination)

        pagination_2: list[int] = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=12,
        )['pagination']

        self.assertEqual([11, 12, 13, 14], pagination_2)

    def test_make_pagination_range_is_static_when_last_page_is_next(self) -> None:  # noqa: E501
        pagination: list[int] = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=18,
        )['pagination']

        self.assertEqual([17, 18, 19, 20], pagination)

        pagination_2: list[int] = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=19,
        )['pagination']

        self.assertEqual([17, 18, 19, 20], pagination_2)

        pagination_3: list[int] = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=21,
        )['pagination']

        self.assertEqual([17, 18, 19, 20], pagination_3)

    def test_pagination_renders_no_recipe_found_if_no_recipes(self) -> None:
        client: Client = Client()
        response: HttpResponse = client.get(
            reverse('recipes:home')
        )
        response_content: str = response.content.decode('utf-8')

        self.assertIn('No recipe found', response_content)

    def test_pagination_renders_correct_amount_of_recipes_per_page(self) -> None:  # noqa: E501
        #  makes ten recipes
        for i in range(10):
            kwargs: dict = {'title': f't-{i}',
                            'slug': f's-{i}',
                            'author': {'username': f'a{i}'}
                            }
            recipe: Recipe = self.make_recipe(**kwargs)  # noqa: F841

        client: Client = Client()
        response: HttpResponse = client.get(
            reverse('recipes:home')
        )

        response_context: Page = response.context['recipes']
        objects_per_page: int = len(response_context.object_list)

        self.assertEqual(objects_per_page, 9)

    # def test_pagination_renders_correct_amount_of_recipes_per_page(self) -> None:  # noqa: E501
    #     #  make ten recipes
    #     for i in range(10):
    #         recipe: Recipe = self.make_recipe(title=f'title-recipes-test-{i}',  # noqa: F841 E501
    #                                           slug=f'title-recipes-test{i}',
    #                                           author={'username': f'adão{i}'},  # noqa: E501
    #                                           )
    #     client: Client = Client()
    #     response: HttpResponse = client.get(
    #         reverse('recipes:home')
    #     )

    #     response_content: str = response.content.decode('utf-8')

    #     amount_recipes_titles: int = 0

    #     for title in response_content.split():
    #         if 'title-recipes-test' in title:
    #             amount_recipes_titles += 1

    #     self.assertEqual(amount_recipes_titles, 9)
