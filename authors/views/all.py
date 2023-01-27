from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.backends.base import SessionBase
from django.http import Http404, HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse

from authors.forms import RegisterForm, LoginForm

from recipes.models import Recipe

from utils.pagination import make_pagination

import os


PER_PAGE_USER = os.environ.get("PER_PAGE_USER", 6)


def register_view(request: HttpRequest) -> render:
    register_form_data: SessionBase = request.session.get('register_form_data',
                                                          None,
                                                          )
    form: RegisterForm = RegisterForm(register_form_data)

    return render(request, 'authors/pages/author.html', context={
        'form': form,
        'form_title': 'Register',
        'form_action': reverse('authors:register_create'),
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
        return redirect(reverse('authors:login'))  # direciona para a página de login  # noqa: E501

    return redirect('authors:register')


def login_view(request) -> render:
    form: LoginForm = LoginForm()

    return render(request, 'authors/pages/login.html', context={
        'form': form,
        'form_title': 'Login',
        'form_action': reverse('authors:login_create'),
    })


def login_create(request) -> None:
    if not request.POST:
        raise Http404()

    form: LoginForm = LoginForm(request.POST)

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if authenticated_user is not None:
            login(request, authenticated_user)
            messages.success(request, 'Login realizado com sucesso')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')

    return redirect('authors:dashboard')


@login_required(redirect_field_name='next', login_url='authors:login')
def logout_view(request) -> None:
    if not request.POST:
        messages.error(request, 'Invalid request')
        return redirect(reverse('authors:login'))

    if request.POST.get('username') != request.user.username:
        messages.error(request, 'Invalid credentials')
        return redirect(reverse('authors:login'))

    logout(request)  # faz o logout
    messages.success(request, 'Logout realizado com sucesso')
    return redirect(reverse('authors:login'))  # redireciona para a página de login  # noqa: E501


@login_required(redirect_field_name='next', login_url='authors:login')
def dashboard(request: HttpRequest) -> render:
    recipes: list[object] = Recipe.objects.filter(author=request.user,
                                                  is_published=False,
                                                  ).order_by('-id')

    page_object, pagination_range = make_pagination(request,
                                                    recipes,
                                                    PER_PAGE_USER,
                                                    )

    return render(request, 'authors/pages/dashboard.html', context={
        'form_title': 'Dashboard',
        'recipes': page_object,
        'pagination_range': pagination_range,
    })


# @login_required(redirect_field_name='next', login_url='authors:login')
# def dashboard_recipe_edit(request: HttpRequest, id: int) -> render:
#     recipe: Recipe = Recipe.objects.get(pk=id,
#                                         author=request.user,
#                                         is_published=False,
#                                         )

#     form: RecipeEditForm = RecipeEditForm(data=request.POST or None,
#                                           files=request.FILES or None,
#                                           instance=recipe,
#                                           )

#     if not recipe:
#         raise Http404()

#     if form.is_valid():
#         data = form.save(commit=False)

#         data.author = request.user
#         data.is_published = False
#         data.preparation_steps_is_html = False

#         data.save()

#         messages.success(request, 'Receita salva com sucesso')

#         return redirect(
#             reverse('authors:dashboard_recipe_edit', args=(id,))
#             )

#     return render(request, 'authors/pages/dashboard_recipe.html', context={
#         'recipe': recipe,
#         'form': form,
#     })


# @login_required(redirect_field_name='next', login_url='authors:login')
# def dashboard_new_recipe(request: HttpRequest) -> render:
#     form: RecipeEditForm = RecipeEditForm(
#         data=request.POST or None,
#         files=request.FILES or None,
#     )  # aqui não usamos o parâmetro instance

#     if form.is_valid():
#         recipe = form.save(commit=False)

#         recipe.author = request.user
#         recipe.preparation_steps_is_html = False
#         recipe.is_published = False

#         recipe.save()

#         messages.success(request, 'Receita salva com sucesso')

#         return redirect(
#             reverse('authors:dashboard')
#         )

#     return render(request, 'authors/pages/dashboard_recipe.html', context={
#         'form': form,
#     })


@login_required(redirect_field_name='next', login_url='authors:login')
def dashboard_delete_recipe(request: HttpRequest) -> render:
    #  checamos se o método e POST
    if not request.POST:
        raise Http404()

    # de dentro de POST, capturamos o id da receita
    POST = request.POST
    id = POST.get('id')

    # selecionamos a receita pelo id, autor e publicação
    recipe: Recipe = Recipe.objects.get(pk=id,
                                        is_published=False,
                                        author=request.user,
                                        )

    # erro caso a receita não tenha sido encontrada
    if not recipe:
        raise Http404()

    # deleta a receita se encontrada e mensagem de sucesso
    recipe.delete()
    messages.success(request, 'Receita deletada com sucesso.')

    # retorna para página inicial da dashboard
    return redirect(
        reverse('authors:dashboard')
        )
