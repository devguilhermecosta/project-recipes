from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_chrome_browser
from selenium.webdriver.chrome.webdriver import WebDriver


class RecipeBaseFunctionalTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser: WebDriver = make_chrome_browser()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()
