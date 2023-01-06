from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_chrome_browser
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class RecipeBaseFunctionalTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser: WebDriver = make_chrome_browser()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()


class RecipeHomePageFunctionalTestCase(RecipeBaseFunctionalTest):
    def test_the_test(self) -> None:
        self.browser.get(self.live_server_url)
        body: WebElement = self.browser.find_element(By.TAG_NAME, 'body')

        self.assertIn('No recipe found', body.text)
