from django.shortcuts import render
from django.http import HttpResponse


def home(request) -> HttpResponse:
    return render(request, 'recipes/home.html')


def about(request) -> HttpResponse:
    return render(request, 'recipes/about.html')


def contact(request) -> HttpResponse:
    return render(request, 'recipes/contato.html')
