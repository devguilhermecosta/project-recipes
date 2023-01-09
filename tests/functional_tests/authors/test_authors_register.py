import pytest
from .base import BaseAuthorsFunctionalTests as BaseAuthor
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from time import sleep


@pytest.mark.functional_test
class AuthorsRegisterFunctionalTests(BaseAuthor):
    def fill_all_fields_dummy_data(self,
                                   form: WebElement,
                                   content: str) -> None:
        '''the content parameter will be written
        to all fields, except email'''

        # seleciona todos os campos do form
        fields: list[WebElement] = form.find_elements(
            By.TAG_NAME,
            'input',
        )

        for field in fields:
            if field.is_displayed():
                if field.get_attribute('name') == 'email':
                    field.send_keys('email@email.com')
                else:
                    field.send_keys(content * 10)

    def get_element_by_placeholder(self,
                                   web_element: WebElement,
                                   placeholder: str,
                                   ) -> WebElement:
        element: WebElement = web_element.find_element(
            By.XPATH,
            f'//input[@placeholder="{placeholder}"]'
        )
        return element

    def test_empty_first_name_field_error_message(self) -> None:
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

        # preenche o field first name
        self.fill_all_fields_dummy_data(form, ' ')

        # clica no botão enviar
        button: WebElement = form.find_element(
            By.XPATH,
            '/html/body/main/div/form/div[7]/button',
        )
        button.click()

        # declaramos novamente o formulário,
        # caso contrário um erro do tipo
        # stale element reference: element is not attached to the page document
        # será levantado
        form_2: WebElement = self.browser.find_element(
            By.XPATH,
            '/html/body/main/div/form',
        )

        self.assertIn('O campo nome é obrigatório', form_2.text)
        self.fail(('Fazer todos os testes para campos vazios. '
                   'Refatorar o teste em pequenas funções. '
                   'Tentar usar parameterized. '
                   'Testar a função de callback. '
                   'Testar o formulário corretamente preenchido. ')
                  )
