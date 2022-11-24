from django.shortcuts import render


def home(request) -> render:
    return render(request, 'recipes/pages/home.html')


def recipes(request, id) -> render:
    return render(request, 'recipes/pages/recipe-view.html')
