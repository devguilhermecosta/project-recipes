from django.views.generic import TemplateView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from authors.models import Profile
from typing import Any


class ProfileView(TemplateView):
    template_name = 'authors/pages/profile.html'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:  # noqa: E501
        context = self.get_context_data(*args, **kwargs)
        profile_id = context.get('id')
        profile_filter = Profile.objects.filter(
            pk=profile_id,
            ).select_related('author')

        profile = get_object_or_404(
            profile_filter, pk=profile_id
        )

        return self.render_to_response({
            **context,
            'profile': profile,
            'form_title': 'Profile',
        })
