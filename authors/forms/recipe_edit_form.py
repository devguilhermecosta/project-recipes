from django import forms
from django.core.exceptions import ValidationError
from recipes.models import Recipe
from collections import defaultdict
from utils.numbers import is_positive_number


class RecipeEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._form_erros: dict[list] = defaultdict(list)

    class Meta:
        model = Recipe
        fields = '__all__'

        exclude = ['is_published',
                   'preparation_steps_is_html',
                   'author',
                   'slug',
                   ]

        widgets = {
            'preparation_time_unit': forms.Select(choices=(
                ('minuto(s)', 'minuto(s)'),
                ('hora(s)', 'hora(s)'),
                ('dia(s)', 'dias(s)')
                )
            ),
            'servings_unit': forms.Select(choices=(
                ('pessoa(s)', 'pessoa(s)'),
                ('porção', 'porção'),
                ('porções', 'porções'),
            )),
            'cover': forms.FileInput(attrs={
                'class': 'RF__image',
                }),
        }

    # também podemos criar as funções de validação indiviual por field
    def clean(self, *args, **kwargs) -> None:
        super_clean = super().clean(*args, **kwargs)
        cleaned_data: dict = self.cleaned_data

        title: str = str(cleaned_data.get('title'))
        description: str = str(cleaned_data.get('description'))
        preparation_time = str(cleaned_data.get('preparation_time'))
        servings = str(cleaned_data.get('servings'))

        if len(title) < 15:
            self._form_erros['title'].append(
                'O título deve ter pelo menos 15 caracteres'
                )

        if title == description:
            self._form_erros['title'].append(
                'O título não pode ser igual à descrição.'
                )
            self._form_erros['description'].append(
                'A descrição não pode ser igual ao título'
            )

        if not is_positive_number(preparation_time):
            self._form_erros['preparation_time'].append(
                'O tempo de preparo deve ser maior que zero'
            )

        if not is_positive_number(servings):
            self._form_erros['servings'].append(
                'O número de porções deve ser maior que zero'
            )

        if self._form_erros:
            raise ValidationError(self._form_erros)

        return super_clean
