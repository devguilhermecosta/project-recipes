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
