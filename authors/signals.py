from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from authors.models import Profile


User = get_user_model()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, *args, **kwargs) -> None:
    # checa se o perfil não está criado ainda.
    # se created for true, o perfil será criado, senão, atualizado.
    if created:
        profile = Profile.objects.create(author=instance)  # linka o usuário ao perfil  # noqa: E501
        profile.save()  # salva o perfil
