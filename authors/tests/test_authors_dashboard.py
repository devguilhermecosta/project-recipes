from django.contrib.auth.models import User
from django.http import HttpResponse
from django.test import TestCase
from django.urls import ResolverMatch, resolve, reverse

from authors import views


class AuthorsDashboardTests(TestCase):
    def test_dashboard_load_correct_url(self) -> None:
        response: str = reverse('authors:dashboard')

        self.assertEqual(response, '/authors/dashboard/')

    def test_dashboard_load_correct_view(self) -> None:
        response: ResolverMatch = resolve(
            reverse('authors:dashboard')
        )

        self.assertEqual(response.func, views.dashboard)

    def test_dashboard_load_correct_template(self) -> None:
        User.objects.create_user(username='gui',
                                 password='123',
                                 )

        self.client.login(
            username='gui',
            password='123'
        )

        response: HttpResponse = self.client.get(
            reverse('authors:dashboard'),
            follow=True,
        )

        self.assertTemplateUsed(response, 'authors/pages/dashboard.html')

    def test_dashboard_status_code_200_ok(self) -> None:
        url: str = reverse('authors:dashboard')

        response: HttpResponse = self.client.get(
            url,
            follow=True
        )

        self.assertEqual(response.status_code, 200)

    def test_dashboard_has_you_are_logged_whit(self) -> None:
        user: User = User.objects.create_user(username='gui',
                                              password='123',
                                              )
        user.save()

        self.client.login(username='gui',
                          password='123',
                          )
        response: HttpResponse = self.client.get(
            reverse('authors:dashboard'),
            follow=True,
        )

        response_c: str = response.content.decode('utf-8')

        self.assertIn('Você está logado como gui',
                      response_c,
                      )
