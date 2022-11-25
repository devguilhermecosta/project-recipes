# from django.db import models

from random import randint

from faker import Faker


def rand_ratio() -> list:
    result: list = [randint(840, 900), randint(473, 573)]
    return result


fake: Faker = Faker('pt_BR')
w: int = rand_ratio()[0]
h: int = rand_ratio()[1]


def make_recipe(number: int):
    n: int = number
    return {
        'title': fake.sentence(nb_words=6),
        'description': fake.sentence(nb_words=12),
        'preparation_time': fake.random_number(digits=2, fix_len=True),
        'preparation_time_unit': 'Minutos',
        'servings': fake.random_number(digits=2, fix_len=True),
        'servings_unit': 'Porção',
        'preparation_steps': fake.text(3000),
        'created_at': fake.date_time(),
        'author': {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
        },
        'category': {
            'name': fake.word(),
        },
        'cover': {
            'url': f'https://source.unsplash.com/random/{w}x{h}?r={n}',
        },
    }
