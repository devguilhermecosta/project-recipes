import os
from django.http import Http404
from django.shortcuts import render
from django.db.models import Q
from utils.pagination import make_pagination
from django.views.generic import ListView, DetailView
from recipes.models import Recipe
from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.utils import translation
from django.utils.translation import gettext as _
from typing import Dict
from tag.models import Tag


PER_PAGE = os.environ.get("PER_PAGE", 9)


class RecipeHomeBase(ListView):
    model = Recipe
    paginate_by = None
    context_object_name = 'recipes'
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'

    def get_queryset(self, *args, **kwargs) -> QuerySet:
        query_set: QuerySet = super().get_queryset(*args, **kwargs)
        query_set = query_set.filter(is_published=True)
        query_set = query_set.select_related('author', 'category')
        query_set = query_set.prefetch_related('tags', 'author__profile')

        return query_set

    def get_context_data(self, *args, **kwargs) -> dict:
        context: dict = super().get_context_data(*args, **kwargs)

        html_language: str = translation.get_language()

        page_object, pagination_range = make_pagination(
            self.request,
            context.get('recipes'),
            PER_PAGE,
        )

        context.update({
            'recipes': page_object,
            'pagination_range': pagination_range,
            'html_language': html_language,
        })

        return context


class RecipeCategory(RecipeHomeBase):
    template_name = 'recipes/pages/category.html'

    def get_queryset(self, *args, **kwargs) -> QuerySet:
        query_set = super().get_queryset(*args, **kwargs)

        query_set = query_set.filter(
            category__id=self.kwargs.get('category_id'),
            is_published=True,
        )

        if not query_set:
            raise Http404()

        return query_set

    def get_context_data(self, *args, **kwargs) -> dict:
        context = super().get_context_data(*args, **kwargs)
        ctx_recipe = context.get('recipes')
        category_translate: str = _('Category')

        context.update(
            {
                'title': f"{ctx_recipe[0].category.name} - {category_translate}",  # noqa
            }
        )

        return context


class RecipeSearch(RecipeHomeBase):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self, *args, **kwargs) -> None:
        query_set = super().get_queryset(*args, **kwargs)

        self.search_term = self.request.GET.get('q', '')

        if not self.search_term:
            raise Http404()

        query_set = query_set.filter(
            Q(
                Q(title__icontains=self.search_term) |
                Q(description__icontains=self.search_term) |
                Q(preparation_steps__icontains=self.search_term),
            ),
            is_published=True,
            )

        return query_set

    def get_context_data(self, *args, **kwargs) -> dict:
        context = super().get_context_data(*args, **kwargs)

        context.update(
            {
                'page_title': f"Buscando por '{self.search_term}'",
                'search_term': self.search_term,
                'aditional_url': f'&q={self.search_term}',
            }
        )

        return context


class RecipeDetailsView(DetailView):
    model = Recipe
    template_name = 'recipes/pages/recipe-view.html'
    context_object_name = 'recipe'

    def get_queryset(self, *args, **kwargs) -> QuerySet:
        query_set: QuerySet = super().get_queryset(*args, **kwargs)

        query_set = query_set.filter(is_published=True)

        if not query_set:
            raise Http404()

        return query_set

    def get_context_data(self, *args, **kwargs) -> dict:
        context = super().get_context_data(*args, **kwargs)

        recipe = context.get('recipe')

        context.update(
            {
                'recipe_details': True,
                'recipe_description': True,
                'title_recipe': f"{recipe.title}",
            }
        )

        return context


class RecipeListViewApi(RecipeHomeBase):
    template_name = 'recipes/pages/home.html'

    def render_to_response(self, *args, **kwargs) -> JsonResponse:
        recipes = self.get_context_data()['recipes']
        recipes_list: Dict = recipes.object_list.values()

        return JsonResponse(
            list(recipes_list),
            safe=False,
        )


class RecipeListViewDetailsApi(RecipeDetailsView):
    def render_to_response(self, *args, **kwargs) -> JsonResponse:
        recipe = self.get_context_data()['recipe']
        recipe_dict: Dict = model_to_dict(recipe)

        del recipe_dict['preparation_steps_is_html']
        del recipe_dict['is_published']

        if recipe_dict.get('cover'):
            recipe_dict['cover'] = (self.request.build_absolute_uri() +
                                    recipe_dict['cover'].url[1:])

        return JsonResponse(
            recipe_dict,
            safe=False,
        )


def theory(request, *args, **kwargs) -> render:
    recipes: Recipe = Recipe.objects.all().order_by('-id')
    recipes_list: list = recipes[0:10]

    context: dict = {
        'recipes': recipes_list,
    }

    return render(
        request,
        'recipes/pages/theory.html',
        context=context,
    )


class RecipeTag(RecipeHomeBase):
    template_name = 'recipes/pages/tags.html'

    def get_queryset(self, *args, **kwargs) -> None:
        query_set = super().get_queryset(*args, **kwargs)
        query_set = query_set.filter(tags__slug=self.kwargs.get('slug', ''))

        return query_set

    def get_context_data(self, *args, **kwargs) -> dict:
        context = super().get_context_data(*args, **kwargs)
        page_title = Tag.objects.filter(
            slug=self.kwargs.get('slug', '')
            ).first()

        if not page_title:
            page_title = 'No recipes found'

        context.update(
            {
                'page_title': page_title,
            }
        )

        return context


# def recipe(request, id) -> render:
#     recipe: Recipe = get_object_or_404(Recipe,
#                                        pk=id,
#                                        is_published=True,
#                                        )

#     return render(request, 'recipes/pages/recipe-view.html', context={
#         'recipe_details': True,
#         'recipe_description': True,
#         'title_recipe': f"{recipe.title}",
#         'recipe': recipe,
#     })


# def category(request, id) -> render:
#     recipes: list = get_list_or_404(Recipe.objects.filter(category__id=id,
#                                                           is_published=True,
#                                                           ).order_by('-id'))

    # page_object, pagination_range = make_pagination(request,
    #                                                 recipes,
    #                                                 PER_PAGE,
    #                                                 )

#     return render(request, 'recipes/pages/category.html', context={
#         'recipes': page_object,
#         'pagination_range': pagination_range,
#         'title': f"{recipes[0].category.name} - Category",
#     })


# def search(request) -> render:
#     search_term: str = request.GET.get('q', '').strip()

#     if not search_term:
#         raise Http404()

#     recipes = Recipe.objects.filter(
#         Q(
#             Q(title__icontains=search_term) |
#             Q(description__icontains=search_term) |
#             Q(preparation_steps__icontains=search_term),
#         ),
#         is_published=True,
#     ).order_by('-id')

    # page_object, pagination_range = make_pagination(request,
    #                                                 recipes,
    #                                                 PER_PAGE)

#     return render(request, 'recipes/pages/search.html', context={
#         'page_title': f"Buscando por '{search_term}'",
#         'search_term': search_term,
#         'recipes': page_object,
#         'pagination_range': pagination_range,
#         'aditional_url': f'&q={search_term}',
#     })
