from django.shortcuts import render
from django.http import HttpRequest
from .forms import RegisterForm


def register_view(request: HttpRequest) -> render:
    if request.POST:
        form: RegisterForm = RegisterForm(request.POST)
    else:
        form = RegisterForm()

    return render(request, 'authors/pages/author.html', context={
        'form': form,
    })
