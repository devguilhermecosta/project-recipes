from django.shortcuts import render
from .forms import RegisterForm


def register_view(request) -> render:
    form: RegisterForm = RegisterForm()

    return render(request, 'authors/pages/author.html', context={
        'form': form,
    })
