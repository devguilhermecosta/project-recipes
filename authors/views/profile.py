from django.views.generic import TemplateView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from authors.models import Profile
from typing import Any


class ProfileView(TemplateView):
    template_name = 'authors/pages/profile.html'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:  # noqa: E501
        context = self.get_context_data(*args, **kwargs)
        # pega o id do perfil
        profile_id = context.get('id')

        # aplica o filter usando o id e
        # usa select_related para buscar tudo de uma vez
        profile_filter = Profile.objects.filter(
            pk=profile_id,
            ).select_related('author')

        # pega o objeto no banco de dados ou Http404() se não existir
        profile = get_object_or_404(
            profile_filter, pk=profile_id
        )

        # retorna um render.
        # estamos desempacotando o context (**context) e adiconando
        # 'profile' e 'form_title' ao context.
        # é uma alternativa ao update()
        return self.render_to_response({
            **context,
            'profile': profile,
            'form_title': 'Profile',
        })
