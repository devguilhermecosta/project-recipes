from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import Http404, HttpRequest
from django.db.models import Q
from . models import Recipe
from utils.pagination import make_pagination


def home(request: HttpRequest) -> render:
    recipes: list[object] = Recipe.objects.filter(is_published=True).order_by('-id')  # noqa: E501

    page_object, pagination_range = make_pagination(request, recipes, 9, 4)

    return render(request, 'recipes/pages/home.html', context={
        'recipes': page_object,
        'pagination_range': pagination_range,
    })


def recipe(request, id) -> render:
    recipe: Recipe = get_object_or_404(Recipe,
                                       pk=id,
                                       is_published=True,
                                       )

    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe_details': True,
        'recipe_description': True,
        'title_recipe': f"{recipe.title}",
        'recipe': recipe,
    })


def category(request, id) -> render:
    recipes: list = get_list_or_404(Recipe.objects.filter(category__id=id,
                                                          is_published=True,
                                                          ).order_by('-id'))

    page_object, pagination_range = make_pagination(request, recipes, 9, 4)

    return render(request, 'recipes/pages/category.html', context={
        'recipes': page_object,
        'pagination_range': pagination_range,
        'title': f"{recipes[0].category.name} - Category",
    })


def search(request) -> render:
    search_term: str = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()

    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term) |
            Q(preparation_steps__icontains=search_term),
        ),
        is_published=True,
    ).order_by('-id')

    page_object, pagination_range = make_pagination(request, recipes, 9, 4)

    return render(request, 'recipes/pages/search.html', context={
        'page_title': f"Buscando por '{search_term}'",
        'search_term': search_term,
        'recipes': page_object,
        'pagination_range': pagination_range,
        'aditional_url': f'&q={search_term}',
    })
