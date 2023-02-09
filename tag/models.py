import string as st
from random import SystemRandom
from django.db import models
from django.utils.text import slugify


class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

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
