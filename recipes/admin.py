from django.contrib import admin
from .models import Category, Recipe


class CategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    # itens de cada receita a ser exibido na tela
    list_display = ['id', 'title', 'created_at', 'is_published', 'author']

    # itens que sustentarão o link de acessa à receita
    list_display_links = ['id', 'title']

    # o sistema de busca irá procuar o termo em:
    search_fields = ['id', 'title', 'description', 'slug', 'preparation_steps']

    # filtros na lateral direita da área adminstrativa
    list_filter = ['category',
                   'author',
                   'is_published',
                   'preparation_steps_is_html',
                   ]

    # objetos por página
    list_per_page = 10

    # itens que podem ser editados sem entrar no objeto
    list_editable = ['is_published']

    # ordenar por (id ou id decrescente)
    ordering = ['-id']

    # preencher o slug automaticamente
    prepopulated_fields = {
        'slug': ['title'],
    }

    # autocomplete_fields
    autocomplete_fields = 'tags',


admin.site.register(Category, CategoryAdmin)
