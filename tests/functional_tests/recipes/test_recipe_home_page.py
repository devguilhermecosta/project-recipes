import pytest
from base import RecipeBaseFunctionalTest
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from recipes.tests.test_recipe_base import RecipeMixin


@pytest.mark.functional_test
class RecipeHomePageFunctionalTestCase(RecipeBaseFunctionalTest, RecipeMixin):
    def test_home_page_whitout_recipes_no_recipe_found(self) -> None:
        self.browser.get(self.live_server_url)
        body: WebElement = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipe found', body.text)
