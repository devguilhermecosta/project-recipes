from django.apps import AppConfig


class AuthorsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authors'

    # novo método
    def ready(self, *args, **kwargs) -> None:
        import authors.signals  # noqa: F401
        super_ready = super().ready(*args, **kwargs)
        return super_ready
