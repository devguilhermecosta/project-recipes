from django.shortcuts import render
from django.http import HttpResponse


def home(request) -> HttpResponse:
    return render(request, 'recipes/home.html')


def about(request) -> HttpResponse:
    return HttpResponse("I'm ate About")


def contact(request) -> HttpResponse:
    return HttpResponse("I'm at Contact")
