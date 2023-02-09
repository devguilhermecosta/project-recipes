from django.test import TestCase
from recipes.models import Recipe, Category
from django.contrib.auth.models import User


class RecipeMixin:
    def make_category(self, name='Category') -> Category:
        return Category.objects.create(name=name)

    def make_author(self,
                    first_name='first name',
                    last_name='last name',
                    username='username',
                    password='123456',
                    email='username@email.com',
                    ) -> User:

        return User.objects.create_user(first_name=first_name,
                                        last_name=last_name,
                                        username=username,
                                        password=password,
                                        email=email,
                                        )

        # continuação do código ->

    def make_recipe(self,
                    title='Recipe title',
                    description='Recipe Description',
                    slug='recipe-slug',
                    preparation_time=30,
                    preparation_time_unit='Minutos',
                    servings=5,
                    servings_unit='Porções',
                    preparation_steps='Preparation Steps',
                    is_published=True,
                    category=None,
                    author=None,
                    ) -> Recipe:

        if category is None:
            category = {}

        if author is None:
            author = {}

        return Recipe.objects.create(
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            is_published=is_published,
            category=self.make_category(**category),
            author=self.make_author(**author),
        )

    def make_recipe_in_batch(self, qty: int = 10) -> list:
        recipes: list = []

        for i in range(qty):
            kwargs: dict = {'title': f'Recipe Title-{i}',
                            'slug': f's-{i}',
                            'author': {'username': f'u{i}'},
                            }
            recipes.append(self.make_recipe(**kwargs))

        return recipes


class RecipeTestBase(TestCase, RecipeMixin):
    def setUp(self) -> None:
        return super().setUp()
