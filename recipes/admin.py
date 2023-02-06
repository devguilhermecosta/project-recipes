from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline
from .models import Category, Recipe
from tag.models import Tag


class CategoryAdmin(admin.ModelAdmin):
    ...


class TagInline(GenericStackedInline):
    model = Tag
    fields = 'name',
    extra = 1


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

    # relacionamentos genéricos
    inlines = [
        TagInline,
    ]


admin.site.register(Category, CategoryAdmin)
