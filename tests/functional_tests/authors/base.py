from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from utils.browser import make_chrome_browser
from time import sleep


class BaseAuthorsFunctionalTests(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser: WebDriver = make_chrome_browser()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def sleep_t(self, time: float = 10) -> None:
        sleep(time)

    def get_element_by_placeholder(self,
                                   web_element: WebElement,
                                   placeholder: str,
                                   ) -> WebElement:
        element: WebElement = web_element.find_element(
            By.XPATH,
            f'//input[@placeholder="{placeholder}"]'
        )
        return element

    def get_body_text(self) -> str:
        element: WebElement = self.browser.find_element(
            By.TAG_NAME,
            'body'
        )

        return element.text

    def fill_all_fields_dummy_data(self,
                                   form: WebElement,
                                   content: str,
                                   length: int = 10) -> None:
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
                    field.send_keys(content * length)
