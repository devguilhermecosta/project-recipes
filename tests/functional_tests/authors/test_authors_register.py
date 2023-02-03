import pytest
from .base import BaseAuthorsFunctionalTests as BaseAuthor
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By


@pytest.mark.functional_test
class AuthorsRegisterFunctionalTests(BaseAuthor):

    def open_register_form(self) -> WebElement:
        # abre o navegador
        self.browser.get(self.live_server_url)

        # clica em cadestre-se
        page_register: WebElement = self.browser.find_element(
            By.XPATH,
            '//a[@aria-label="cadastrar"]'
        )
        page_register.click()

        # pega o formulário pelo XPATH
        form: WebElement = self.browser.find_element(
            By.XPATH,
            '/html/body/main/div/form',
        )

        return form

    def test_empty_fields_error_messages(self) -> None:
        # pega o formulário de cadastro
        form: WebElement = self.open_register_form()

        # preenche o field first name
        self.fill_all_fields_dummy_data(form, ' ')

        # clica no botão enviar
        form.submit()

        # declaramos novamente o formulário,
        # caso contrário um erro do tipo
        # stale element reference: element is not attached to the page document
        # será levantado
        form_2: WebElement = self.browser.find_element(
            By.XPATH,
            '/html/body/main/div/form',
        )

        error_messages: list = [
            'O campo nome é obrigatório',
            'O campo sobrenome é obrigatório',
            'O campo usuário é obrigatório',
            'O campo senha é obrigatório',
            'O campo repita a senha é obrigatório'
        ]

        for message in error_messages:
            self.assertIn(message, form_2.text)

    def test_fields_filled_correctly_succes_message(self) -> None:
        form: WebElement = self.open_register_form()

        fields: dict = {
            'Digite seu nome': 'Guilherme',
            'Digite seu sobrenome': 'Costa',
            'Digite seu usuário': 'guicosta',
            'Digite seu e-mail': 'email@email.com',
            'Digite a senha': 'Password123@@',
            'Repita a senha': 'Password123@@',
        }

        for placeholder, content in fields.items():
            element: WebElement = self.get_element_by_placeholder(
                form,
                placeholder,
                )
            element.send_keys(content)

        form.submit()

        form_2: WebElement = self.browser.find_element(
            By.TAG_NAME,
            'body',
        )

        self.assertIn('Usuário criado com sucesso.', form_2.text)
