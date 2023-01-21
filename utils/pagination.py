import math
from django.core.paginator import Paginator
from django.http import HttpRequest
from typing import Any


def make_pagination_range(page_range: list[int],
                          qty_pages: int,
                          current_page: int,
                          ) -> dict:
    middle_range: int = math.ceil(qty_pages / 2)
    start_range: int = current_page - middle_range
    stop_range: int = current_page + middle_range
    total_pages: int = len(page_range)

    start_range_offset: int = abs(start_range) if start_range < 0 else 0

    if start_range < 0:
        start_range = 0
        stop_range += start_range_offset

    if stop_range >= total_pages:
        start_range = start_range - abs(stop_range - total_pages)

    if len(page_range) <= qty_pages:
        start_range = 0
        stop_range = len(page_range)

    pagination = page_range[start_range:stop_range]

    return {
        'pagination': pagination,
        'page_range': page_range,
        'qty_pages': qty_pages,
        'current_page': current_page,
        'total_pages': total_pages,
        'start_range': start_range,
        'stop_range': stop_range,
        'first_page_out_of_range': current_page > middle_range and len(page_range) > qty_pages,  # noqa: E501
        'last_page_out_of_range': stop_range < total_pages,
    }


def make_pagination(request: HttpRequest,
                    query_set: list[object] | Any,
                    qty_objects: int | str,
                    per_page: int = 4,
                    ) -> Paginator:
    paginator: Paginator = Paginator(query_set, qty_objects)

    try:
        current_page: int = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1

    page_object: Paginator = paginator.get_page(current_page)

    pagination_range: dict = make_pagination_range(paginator.page_range,
                                                   per_page,
                                                   current_page,
                                                   )
    return page_object, pagination_range
