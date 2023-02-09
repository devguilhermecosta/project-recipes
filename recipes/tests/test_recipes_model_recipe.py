from .test_recipe_base import RecipeTestBase
from recipes.models import Recipe
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from parameterized import parameterized


class RecipeTestModel(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe: Recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_no_defaults(self) -> Recipe:
        recipe = Recipe.objects.create(
            title='Recipe title',
            description='Recipe Description',
            slug='test-de-recipe',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='Porções',
            preparation_steps='Preparation Steps',
            category=self.make_category(name='Test Category'),
            author=self.make_author(first_name='João',
                                    last_name='Silva',
                                    username='joãomaria',
                                    ),
        )
        recipe.full_clean()
        recipe.save()
        return recipe

    @parameterized.expand([
        ('title', 65),
        ('description', 165),
        ('preparation_time_unit', 165),
        ('servings_unit', 65),
    ])
    def test_recipes_fields_max_length(self, field, max_length) -> None:
        setattr(self.recipe, field, 'A' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_field_preparation_steps_is_html_by_default(self) -> None:
        recipe = self.make_recipe_no_defaults()

        self.assertFalse(recipe.preparation_steps_is_html)

    def test_recipe_field_is_published_is_false_by_default(self) -> None:
        recipe = self.make_recipe_no_defaults()

        self.assertFalse(recipe.is_published)

    def test_recipe_string_representation_is_title_field(self) -> None:
        self.recipe.title = 'Recipe title'
        self.recipe.full_clean()
        self.recipe.save()

        self.assertEqual(str(self.recipe), 'Recipe title')

    def test_recipe_field_slug_is_unique(self) -> None:
        needed_text_slug: str = 'slug-recipe-test'
        recipe: Recipe = self.make_recipe(slug=needed_text_slug,
                                          author={'username': 'catarina'},
                                          )
        recipe.save()

        with self.assertRaises(IntegrityError):
            recipe2: Recipe = self.make_recipe(slug=needed_text_slug,
                                               author={'username': 'cat'},
                                               )
            recipe2.save()
