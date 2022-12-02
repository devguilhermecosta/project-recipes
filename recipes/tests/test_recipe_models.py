from .test_recipe_base import RecipeTestBase
from recipes.models import Recipe
from django.core.exceptions import ValidationError


class RecipeTestModel(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe: Recipe = self.make_recipe()
        return super().setUp()

    def test_recipe_title_raises_error_has_more_than_65_char(self) -> None:
        self.recipe.title = 'A' * 70
        self.recipe.slug = 'sdasdasdsdsa'

        with self.assertRaises(ValidationError):
            self.recipe.full_clean()
