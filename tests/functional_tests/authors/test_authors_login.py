import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from .base import BaseAuthorsFunctionalTests as BaseAutor


@pytest.mark.functional_test
class AuthorsLoginFunctionalTests(BaseAutor):

    def test_login_error_message_if_method_not_post(self) -> None:
        # usuário tentar fazer requisição get
        self.browser.get(
            self.live_server_url + reverse('authors:login_create')
        )

        self.assertIn('Not Found',
                      self.get_body_text()
                      )

    def test_login_error_message_if_invalid_credentials(self) -> None:
        # usuário abre o navegador
        self.browser.get(self.live_server_url)

        # usuário clica em faça login
        self.browser.find_element(
            By.XPATH,
            '/html/body/header/div[1]/p/a[2]'
        ).click()

        # usuário fictício
        user: User = User.objects.create_user(username='gui',
                                              password='123456',
                                              )
        user.save()

        # usuário preenche usuário e senha
        form: WebElement = self.browser.find_element(
            By.CLASS_NAME,
            'form',
        )

        username: WebElement = self.get_element_by_placeholder(
            form,
            'Digite seu usuário'
        )
        username.send_keys(user.username)

        password: WebElement = self.get_element_by_placeholder(
            form,
            'Digite sua senha'
        )
        password.send_keys('12345')  # senha incorreta

        # usuário clica em enviar
        form.submit()

        self.assertIn(
            'Usuário ou senha inválidos.',
            self.browser.find_element(
                By.TAG_NAME,
                'body').text
        )

    def test_login_succes_message(self) -> None:
        # usuário entra na home
        self.browser.get(self.live_server_url)

        # usuário clica em faça login
        self.browser.find_element(
            By.XPATH,
            '/html/body/header/div[1]/p/a[2]'
        ).click()

        # usuário fictício
        password: str = '123456'
        user: User = User.objects.create_user(username='patrik',
                                              password=password,
                                              )

        # usuário digita o login e senha
        form: WebElement = self.browser.find_element(
            By.CLASS_NAME,
            'form',
        )
        self.get_element_by_placeholder(
            form, 'Digite seu usuário',
        ).send_keys(user.username)

        self.get_element_by_placeholder(
            form,
            'Digite sua senha',
        ).send_keys(password)

        # usuário clica em enviar
        form.submit()

        self.assertIn('Login realizado com sucesso',
                      self.get_body_text(),
                      )
