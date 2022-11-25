from django.shortcuts import render
from . models import make_recipe


def home(request) -> render:
    return render(request, 'recipes/pages/home.html', context={
        'recipes': [make_recipe(i) for i in range(10)],
    })


def recipes(request, id) -> render:
    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe_details': True,
        'recipe_description': True,
        'recipe': make_recipe(1),
    })
