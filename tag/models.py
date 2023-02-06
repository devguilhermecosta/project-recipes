import string as st
from random import SystemRandom
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify


class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    # Aqui começam os campos para a relação genérica

    # Representa os models que queremos encaixar aqui
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    # Representa o id da linha do model descrito acima
    object_id = models.CharField(max_length=255)

    # Um campo que representa a relação genéria que conhece os campos
    # acima (content_type e object_id)
    content_objects = GenericForeignKey('content_type', 'object_id')

    def save(self, *args, **kwargs) -> str:
        if not self.slug:
            range_letter: str = ''.join(
                SystemRandom().choices(
                    st.ascii_letters + st.digits,
                    k=5
                ),
                )
            self.slug = slugify(f'{self.name}-{range_letter}')
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name
