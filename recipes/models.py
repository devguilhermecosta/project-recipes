from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=65,
                            verbose_name='Nome',
                            )

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=65,)
    description = models.CharField(max_length=165,)
    slug = models.SlugField(max_length=65, unique=True)
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=165,)
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=65,)
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(upload_to='recipes/covers/%Y/%m/%d/',
                              blank=True,
                              default='',
                              )
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True,
                                 default=None,
                                 )
    author = models.ForeignKey(User,
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True,
                               default=None,
                               )

    def __str__(self) -> str:
        return self.title
