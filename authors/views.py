from django.contrib.sessions.backends.base import SessionBase
from django.shortcuts import render, redirect
from django.http import HttpRequest, Http404
from django.contrib import messages
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
    form: RegisterForm = RegisterForm(post)

    if form.is_valid():  # checa se o formulário é válido
        form.save()  # salva na base de dados
        messages.success(request, 'Usuário criado com sucesso.')  # informa que o usuário foi criado  # noqa: E501

        del request.session['register_form_data']  # deleta os dados dos campos

    return redirect('authors:register')
