from unittest import TestCase
from utils.pagination import make_pagination_range


class TestRecipePagination(TestCase):
    def test_make_pagination_range_returns_a_pagination_range(self) -> None:
        pagination: list[int] = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1,
        )['pagination']

        self.assertEqual([1, 2, 3, 4], pagination)

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

    def test_fail(self) -> None:
        self.fail('Fazer uma documentação de como criar uma paginação'
                  'no Django e também fazer os testes do paginator'
                  'e fazer o coverage'
                  )
