from django.shortcuts import render, get_list_or_404
from . models import Recipe


def home(request) -> render:
    recipes: object = Recipe.objects.all().order_by('-id')

    return render(request, 'recipes/pages/home.html', context={
        'recipes': recipes,
    })


def recipe(request, id) -> render:
    recipe: object = Recipe.objects.filter(pk=id).order_by('-id')

    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe_details': True,
        'recipe_description': True,
        'recipe': recipe.first(),
    })
    

def category(request, id) -> render:
    recipe: list = get_list_or_404(Recipe.objects.filter(category__id=id,
                                                         is_published=True,
                                                         ).order_by('-id'))
    
    return render(request, 'recipes/pages/category.html', context={
        'recipes': recipe,
    })
