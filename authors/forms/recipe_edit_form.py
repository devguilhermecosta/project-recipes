from django import forms
from recipes.models import Recipe


class RecipeEditForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'

        exclude = ['is_published',
                   'preparation_steps_is_html',
                   'author',
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
