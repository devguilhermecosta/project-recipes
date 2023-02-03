from django.views import View
from recipes.models import Recipe
from authors.forms import RecipeEditForm
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import Http404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(
    login_required(redirect_field_name='next', login_url='authors:login'),
    name='dispatch',
)
class DashboardRecipe(View):
    def get_recipe(self, id=None):
        recipe = None

        if id is not None:
            recipe = Recipe.objects.get(pk=id,
                                        author=self.request.user,
                                        is_published=False,
                                        )

            if not recipe:
                raise Http404()

        return recipe

    def render_recipe(self, form) -> render:
        return render(self.request,
                      'authors/pages/dashboard_recipe.html',
                      context={
                          'form': form,
                          }
                      )

    def get(self, request, id=None) -> None:
        recipe = self.get_recipe(id)
        form: RecipeEditForm = RecipeEditForm(instance=recipe)

        return self.render_recipe(form)

    def post(self, request, id=None) -> None:
        recipe: Recipe = self.get_recipe(id)

        form: RecipeEditForm = RecipeEditForm(
            data=request.POST or None,
            files=request.FILES or None,
            instance=recipe,
            )

        if form.is_valid():
            recipe = form.save(commit=False)

            recipe.author = request.user
            recipe.is_published = False
            recipe.preparation_steps_is_html = False

            recipe.save()

            messages.success(request, 'Receita salva com sucesso')

            return redirect(
                reverse('authors:dashboard_recipe_edit', args=(recipe.id,))
                )

        self.render_recipe(form)


@method_decorator(
    login_required(redirect_field_name='next', login_url='authors:login'),
    name='dispatch'
)
class DashboardRecipeDelete(DashboardRecipe):
    def post(self, *args, **kwargs) -> redirect:
        recipe = self.get_recipe(kwargs.get('id'))
        recipe.delete()

        messages.success(self.request, 'Receita deletada com sucesso')

        return redirect(
            reverse('authors:dashboard')
        )
