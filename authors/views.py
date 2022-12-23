from django.contrib.sessions.backends.base import SessionBase
from django.shortcuts import render, redirect
from django.http import HttpRequest, Http404
from .forms import RegisterForm


def register_view(request: HttpRequest) -> render:
    register_form_data: SessionBase = request.session.get('register_form_data',
                                                          None,
                                                          )
    form: RegisterForm = RegisterForm(register_form_data)

    return render(request, 'authors/pages/author.html', context={
        'form': form,
    })


def register_create(request: HttpRequest) -> dict:
    if not request.POST:
        raise Http404()

    post: dict = request.POST
    request.session['register_form_data'] = post
    form: RegisterForm = RegisterForm(post)  # noqa: F841

    return redirect('authors:register')
