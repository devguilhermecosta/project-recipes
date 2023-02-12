from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from .models import Recipe
import os


def delete_cover(instance: Recipe):
    try:
        os.remove(instance.cover.path)
    except (ValueError, FileNotFoundError):
        ...


@receiver(pre_delete, sender=Recipe)
def recipe_cover_delete(sender, instance, *args, **kwargs):
    old_instance = Recipe.objects.filter(pk=instance.pk).first()
    delete_cover(old_instance)


@receiver(pre_save, sender=Recipe)
def recipe_cover_update(sender, instance: Recipe, *args, **kwargs) -> None:
    old_instance = Recipe.objects.filter(pk=instance.pk).first()
    new_instance: bool = old_instance.cover != instance.cover

    if new_instance:
        delete_cover(old_instance)
