from django.shortcuts import render
from . models import make_recipe, Recipe


def home(request) -> render:
    recipes: object = Recipe.objects.all().order_by('-id')
    return render(request, 'recipes/pages/home.html', context={
        'recipes': recipes,
    })


def recipes(request, id) -> render:
    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe_details': True,
        'recipe_description': True,
        'recipe': make_recipe(1),
    })
