import pytest
from base import RecipeBaseFunctionalTest
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


@pytest.mark.functional_test
class RecipeHomePageFunctionalTestCase(RecipeBaseFunctionalTest):
    def test_home_page_whitout_recipes_no_recipe_found(self) -> None:
        self.browser.get(self.live_server_url)
        body: WebElement = self.browser.find_element(By.TAG_NAME, 'body')

        self.assertIn('No recipe found', body.text)
