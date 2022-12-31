from django.contrib.sessions.backends.base import SessionBase
from django.shortcuts import render, redirect
from django.http import HttpRequest, Http404
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import RegisterForm


def register_view(request: HttpRequest) -> render:
    register_form_data: SessionBase = request.session.get('register_form_data',
                                                          None,
                                                          )
    form: RegisterForm = RegisterForm(register_form_data)

    return render(request, 'authors/pages/author.html', context={
        'form': form,
        'form_action': reverse('authors:create'),
    })


def register_create(request: HttpRequest) -> dict:
    if not request.POST:
        raise Http404()

    post: dict = request.POST
    request.session['register_form_data'] = post
    form: RegisterForm = RegisterForm(post)

    if form.is_valid():  # checa se o formulário é válido
        user: User = form.save(commit=False)  # captura os dados do form em um commit falso  # noqa: E501
        user.set_password(user.password)  # criptografa a senha
        user.save()  # salva na base de dados
        messages.success(request, 'Usuário criado com sucesso.')  # informa que o usuário foi criado  # noqa: E501

        del request.session['register_form_data']  # deleta os dados dos campos

    return redirect('authors:register')
