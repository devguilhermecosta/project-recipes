from .test_recipe_base import RecipeTestBase
from recipes.models import Category
from django.core.exceptions import ValidationError


class CategoryTestModel(RecipeTestBase):
    def setUp(self) -> None:
        self.category: Category = self.make_category(
            name='Recipe Category',
        )
        return super().setUp()

    def test_recipe_category_string_representation_is_name_field(self) -> None:
        self.assertEqual(str(self.category), 'Recipe Category')

    def test_recipe_category_name_field_max_length_is_65(self) -> None:
        self.category.name = 'A' * 66

        with self.assertRaises(ValidationError):
            self.category.full_clean()
